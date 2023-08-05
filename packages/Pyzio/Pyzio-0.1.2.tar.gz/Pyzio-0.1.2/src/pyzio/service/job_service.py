from typing import List

from ..port.adapter.brainer_client import BrainerClient
from ..pyzio_printer import PyzioPrinter
from ..repository.local_job_repository import LocalJobRepository, Job
from ..repository.printer_state_repository import PrinterStateRepository


class JobService:

	def __init__(self,
				 printer: PyzioPrinter,
				 brainer_client: BrainerClient,
				 local_job_repo: LocalJobRepository,
				 printer_state_repo: PrinterStateRepository):
		self._printer = printer
		self._brainer_client = brainer_client
		self._local_job_repo = local_job_repo
		self._printer_state_repo = printer_state_repo

	def queue_jobs(self, jobs: List[Job]) -> None:
		self._local_job_repo.update_jobs(jobs)

	def start_next_job(self) -> bool:
		if not self._local_job_repo.is_queue_empty():
			job = self._local_job_repo.get_job_from_queue()
			printer_id, secret = self._printer_state_repo.get_printer_id(), self._printer_state_repo.get_secret()
			self._brainer_client.get_file(printer_id, secret, job.job_id, job.filename, job.cluster_id)
			self._printer.start_printing(job.job_id)
			return True
		return False
