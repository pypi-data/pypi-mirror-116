"""
Translation support
"""
import collections
import os
from logging import Logger
from typing import Optional, List, Tuple, Set

from ruamel import yaml

from mcdreforged.constants import core_constant
from mcdreforged.minecraft.rtext import RTextBase, RTextList
from mcdreforged.utils import file_util, translation_util
from mcdreforged.utils.logger import DebugOption
from mcdreforged.utils.types import TranslationStorage, MessageText

LANGUAGE_RESOURCE_DIRECTORY = os.path.join('resources', 'lang')
HERE = os.path.abspath(os.path.dirname(__file__))
LANGUAGE_DIRECTORY = os.path.join(HERE, LANGUAGE_RESOURCE_DIRECTORY)


class TranslationManager:
	def __init__(self, logger: Logger):
		self.logger = logger
		self.language = core_constant.DEFAULT_LANGUAGE
		self.translations: TranslationStorage = collections.defaultdict(dict)
		self.available_languages: Set[str] = set()

	def load_translations(self):
		self.translations.clear()
		self.available_languages.clear()
		for file_path in file_util.list_file_with_suffix(LANGUAGE_DIRECTORY, core_constant.LANGUAGE_FILE_SUFFIX):
			language, _ = os.path.basename(file_path).rsplit('.', 1)
			try:
				with open(os.path.join(LANGUAGE_DIRECTORY, file_path), encoding='utf8') as file_handler:
					translations = dict(yaml.load(file_handler, Loader=yaml.Loader))
				for key, text in translations.items():
					self.translations[key][language] = text
				self.available_languages.add(language)
				self.logger.debug('Loaded translation for {} with {} entries'.format(language, len(translations)), option=DebugOption.MCDR)
			except:
				self.logger.exception('Failed to load language {} from "{}"'.format(language, file_path))

	def set_language(self, language: str):
		self.language = language
		if language not in self.available_languages:
			self.logger.warning('Setting language to {} with 0 available translation'.format(language))

	def translate(self, key: str, args: tuple, kwargs: dict, *, allow_failure: bool, language: Optional[str] = None, fallback_language: Optional[str] = None, plugin_translations: Optional[TranslationStorage] = None) -> MessageText:
		if language is None:
			language = self.language
		if plugin_translations is None:
			plugin_translations = {}

		# Translating
		try:
			translated_text = translation_util.translate_from_dict(self.translations.get(key, {}), language, fallback_language=fallback_language)
		except KeyError:
			translated_text = translation_util.translate_from_dict(plugin_translations.get(key, {}), language, fallback_language=fallback_language, default=None)

		# Check if there's any rtext inside args
		use_rtext = False
		for arg in args:
			if isinstance(arg, RTextBase):
				use_rtext = True

		# Processing
		if translated_text is not None:
			translated_text = translated_text.strip('\n\r')
			if use_rtext:
				translated_text = self.__apply_args(translated_text, args, kwargs)
			else:
				translated_text = translated_text.format(*args, **kwargs)
			return translated_text
		else:
			if not allow_failure:
				raise KeyError('Translation key "{}" not found'.format(key))
			self.logger.error('Error translate text "{}" to language {}'.format(key, language))
			return key if not use_rtext else RTextBase.from_any(key)

	@classmethod
	def __apply_args(cls, translated_text: str, args: tuple, kwargs: dict) -> RTextBase:
		args = list(args)
		kwargs = kwargs.copy()
		counter = 0
		rtext_elements = []  # type: List[Tuple[str, RTextBase]]

		def get():
			nonlocal counter
			rv = '@@MCDR#Translation#Placeholder#{}@@'.format(counter)
			counter += 1
			return rv

		for i, arg in enumerate(args):
			if isinstance(arg, RTextBase):
				placeholder = get()
				rtext_elements.append((placeholder, arg))
				args[i] = placeholder
		for key, value in kwargs.items():
			if isinstance(value, RTextBase):
				placeholder = get()
				rtext_elements.append((placeholder, value))
				kwargs[key] = placeholder

		texts = [translated_text.format(*args, **kwargs)]
		for placeholder, rtext in rtext_elements:
			new_texts = []
			for text in texts:
				processed_text = []
				if isinstance(text, str):
					for j, ele in enumerate(text.split(placeholder)):
						if j > 0:
							processed_text.append(rtext)
						processed_text.append(ele)
				else:
					processed_text.append(text)
				new_texts.extend(processed_text)
			texts = new_texts
		return RTextList(*texts)
