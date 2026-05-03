from typing import Any, Dict

class DictMixin:
    __table__: Any

    def to_dict(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }