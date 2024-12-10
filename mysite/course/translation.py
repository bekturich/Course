from .models import Category, Course
from modeltranslation.translator import TranslationOptions, register


@register(Course)
class CourseTranslationOp(TranslationOptions):
    fields = ['description']


@register(Category)
class CategoryTranslationsOp(TranslationOptions):
    fields = ['category_name']
