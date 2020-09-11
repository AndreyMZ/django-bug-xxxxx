import asyncio
import os

import django
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from polls.models import Question, Choice

N = 100
M = 10


class Command(BaseCommand):
	def handle(self, *args, **options):
		if django.VERSION >= (3, 0):
			# https://docs.djangoproject.com/en/3.1/topics/async/#envvar-DJANGO_ALLOW_ASYNC_UNSAFE
			os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

		asyncio.run(handle_async())


async def handle_async():
	with transaction.atomic():
		Question.objects.all().delete()

		async def _process_task(i):
			await asyncio.sleep(0) # Real application would make e.g. an async HTTP request here.
			with transaction.atomic():
				question = Question.objects.create(question_text=f"demo question {i}", pub_date=timezone.now())
				for j in range(N // M - 1):
					Choice.objects.create(question=question, choice_text=f"demo choice {i}.{j}")

		tasks = [_process_task(i) for i in range(M)]
		await asyncio.gather(*tasks)
