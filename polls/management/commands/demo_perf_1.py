import asyncio
import os
import time

import django
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from polls.models import Question, Choice

N = 1000

class Command(BaseCommand):
	def handle(self, *args, **options):
		if django.VERSION >= (3, 0):
			os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

		Question.objects.all().delete()

		start = time.time()
		with transaction.atomic():
			asyncio.run(handle_async())
		end = time.time()

		print(f"Django {django.__version__}: {end - start}")


async def handle_async():
	await asyncio.sleep(0)
	question = Question.objects.create(question_text=f"demo question", pub_date=timezone.now())
	for j in range(N - 1):
		Choice.objects.create(question=question, choice_text=f"demo choice {j}")
