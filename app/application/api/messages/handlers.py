from fastapi import APIRouter, status, HTTPException

from application.api.dependencies.containers import container
from application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post(
    "/", 
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint creating new chat. If chat title exists, 400 status code raises.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
    }
)
async def create_chat_handler(schema: CreateChatRequestSchema):
    ''' Create new chat. '''
    mediator = container.resolve(Mediator)
    
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": exception.message
            }
        )
        
    return CreateChatResponseSchema.from_entity(chat)