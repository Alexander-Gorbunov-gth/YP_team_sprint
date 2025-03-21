from pydantic import BaseModel, Field


class Permissions(BaseModel):
    films_can_view: str = Field(default="films_can_view")
    films_can_edit: str = Field(default="films_can_edit")
    films_can_delete: str = Field(default="films_can_delete")

    genres_can_view: str = Field(default="genres_can_view")
    genres_can_edit: str = Field(default="genres_can_edit")
    genres_can_delete: str = Field(default="genres_can_delete")

    persons_can_view: str = Field(default="persons_can_view")
    persons_can_edit: str = Field(default="persons_can_edit")
    persons_can_delete: str = Field(default="persons_can_delete")


permissions = Permissions()
