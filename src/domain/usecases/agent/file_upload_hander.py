from dataclasses import dataclass

from fastapi import UploadFile

from src.core.exceptions.upload_file_exception import FileLargeException
from src.core.utils.save_file import SaveFileHandler
from src.domain.usecases.base import BaseUseCase, UseCaseResult


@dataclass
class FileUploadUseCaseInput:
    user_id: int
    agent_id: int
    file: UploadFile


@dataclass
class FileUploadUseCaseOutput:
    directory_path: str
    file_path: str
    file_size: int
    content_type: str


class FileUploadUseCase(BaseUseCase[FileUploadUseCaseInput, FileUploadUseCaseOutput]):
    def __init__(self, save_file_handler: SaveFileHandler):
        self.save_file_handler = save_file_handler

    async def execute(
        self, input_data: FileUploadUseCaseInput
    ) -> UseCaseResult[FileUploadUseCaseOutput]:
        try:
            directory_path = self.save_file_handler.create_agent_directory(
                input_data.user_id, input_data.agent_id
            )

            # Convert file to hex
            file_hex = await self.save_file_handler.convert_to_hex(input_data.file)

            # save file
            file_path, content_type = self.save_file_handler.save_uploaded_file(
                file_hex, directory_path
            )

            return UseCaseResult.success_result(
                FileUploadUseCaseOutput(
                    directory_path=directory_path,
                    file_path=file_path,
                    file_size=file_hex.size,
                    content_type=content_type,
                )
            )

        except FileLargeException as e:
            self.save_file_handler.cleanup_file_on_error(file_path)
            self.logger.warning(str(e))
            return UseCaseResult.error_result("File is too large", e)

        except Exception as e:
            self.save_file_handler.cleanup_file_on_error(file_path)
            self.logger.error(str(e))
            return UseCaseResult.error_result(
                "Unexpected error in file upload usecase", e
            )
