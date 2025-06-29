from fastapi import APIRouter

router = APIRouter(prefix="/templates")


@router.get("/{template_id}/preview")
async def preview_template(template_id: str) -> str:
    return f"Preview {template_id}"
