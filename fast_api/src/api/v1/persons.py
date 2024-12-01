from http import HTTPStatus
import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from src.models.person import Person
from src.services.persons import PersonService, get_person_service

logger = logging.getLogger(__name__)

router = APIRouter()

