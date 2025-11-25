from enum import Enum


class PullRequestStatus(str, Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"


class Error(Enum):
    TEAM_EXISTS = "Команда уже существует"
    PR_EXISTS = "PR уже существует"
    USER_EXISTS = "Пользователь уже существует"
    PR_MERGED = "Нельзя менять ревьюверов после MERGED"
    NOT_ASSIGNED = "Пользователь не был назначен ревьювером"
    NO_CANDIDATE = "Нет доступных кандидатов"
    TEAM_NOT_FOUND = "Команда не найдена"
    USER_NOT_FOUND = "Пользователь не найден"
    AUTHOR_NOT_FOUND = "Автор не найден"
    PR_NOT_FOUND = "PR не найден"
    REVIEWER_NOT_FOUND = "Ревьювер не найден"

    @property
    def details(self) -> dict[str, str]:
        return {"code": self.name, "message": self.value}
