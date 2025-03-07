# import uuid
# from pathlib import Path
# from typing import Annotated

# from dependency_injector.wiring import inject, Provide
# from fastapi import Depends
# from src.services.users.injective import Container
# from src.services.users.interfacies import IUserService


# @inject
# async def user_by_id(
#     # current_user=Depends(get_current_user),
#     user_id: Annotated[uuid.UUID, Path],
#     user_services: IUserService = Depends(Provide[Container.user_service]),
# ):
#     return await user_services.get_user(current_user=None, user_id=user_id)
