# views.py
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import Meeting, Project, Machine
from .serializer import ProjectSerializer, MachineSerializer
from samples.models import UserMachineModel
import json

from .serializer import MeetingSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer



@require_http_methods(["GET"])
def meeting_list(request):
    meetings = Meeting.objects.all().values('id', 'title', 'description', 'date', 'location', 'participants')
    meetings_list = []
    for meeting in meetings:
        participants = list(UserMachineModel.objects.filter(meetings=meeting['id']).values('id', 'username', 'email'))
        meeting['participants'] = participants
        meetings_list.append(meeting)
    return Response(meetings_list)

@csrf_exempt
@require_http_methods(["POST"])
def meeting_create(request):
    data = json.loads(request.body)
    participants_ids = data.pop('participants', [])
    participants = UserMachineModel.objects.filter(id__in=participants_ids)
    meeting = Meeting.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
        location=data.get('location')
    )
    meeting.participants.set(participants)
    meeting.save()
    return Response({
        'id': meeting.id,
        'title': meeting.title,
        'description': meeting.description,
        'date': meeting.date,
        'location': meeting.location,
        'participants': list(meeting.participants.values('id', 'username', 'email'))
    })

@csrf_exempt
@require_http_methods(["PUT"])
def meeting_update(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    data = json.loads(request.body)
    participants_ids = data.pop('participants', [])
    participants = UserMachineModel.objects.filter(id__in=participants_ids)
    meeting.title = data.get('title', meeting.title)
    meeting.description = data.get('description', meeting.description)
    meeting.date = data.get('date', meeting.date)
    meeting.location = data.get('location', meeting.location)
    meeting.participants.set(participants)
    meeting.save()
    return Response({
        'id': meeting.id,
        'title': meeting.title,
        'description': meeting.description,
        'date': meeting.date,
        'location': meeting.location,
        'participants': list(meeting.participants.values('id', 'username', 'email'))
    })


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class VersionAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"version": settings.VERSION})

