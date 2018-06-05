from problemstatements.models import ProblemStatement, Solution, Mentor, Sponsor, ProblemStatementPlaylist
from users.models import User
from problemstatements.serializers import ProblemStatementSerializer, ProblemStatementPlaylistSerializer
from rest_framework import generics
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

class ProblemStatementList(generics.ListCreateAPIView):
    queryset = ProblemStatement.objects.all()
    serializer_class = ProblemStatementSerializer

class ProblemStatementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProblemStatement.objects.all()
    serializer_class = ProblemStatementSerializer

class ProblemStatementPlaylistList(generics.ListCreateAPIView):
    queryset = ProblemStatementPlaylist.objects.all()
    serializer_class = ProblemStatementPlaylistSerializer

@csrf_exempt 
def problemSpecificSolution(request,pk):

    if(request.method == 'POST'):

        return HttpResponse(request.body)

    else:
        Problem = ProblemStatement.objects.get(pk = pk)
        Sol = Solution.objects.filter(problemStatement=Problem)
        Men = Mentor.objects.filter(problemStatement=Problem)
        Spo = Sponsor.objects.filter(problemStatement=Problem)

        Problem = model_to_dict(Problem)
        ret_Problem = {'time_to_show': Problem['time_to_show']  , 'id': Problem['id'] , 'description': Problem['description'], 'domain':Problem['domain'] , 'videolink': Problem['videolink'], 'title': Problem['title']}            

        x = []
        for j in Sol:
            x.append(model_to_dict(j))
        
        y = []
        for j in Men:
            y.append(model_to_dict(j))

        z = []
        for j in Spo:
            z.append(model_to_dict(j))

        ret = { "Problemstatement": ret_Problem, "Solutions": x, "Mentors": y, "Sponsors": z }
        return JsonResponse(ret)

@csrf_exempt
@api_view(['POST', ])
def postSolution(request,pk):

    User_instance = User.objects.get( email = request.data['user_email'] )
    ProblemStatement_instance = ProblemStatement.objects.get(pk=pk)
    Solution.objects.create( contestant= User_instance, problemStatement=ProblemStatement_instance, category=request.data['category'], is_team=request.data['is_team'], team_name=request.data['team_name'], team_size=request.data['team_size'], video_solution=request.data['video_solution'] )
    # console.log( contestant=request.body.user_email, ProblemStatement=pk, category=request.body.contestant, is_team=request.body.is_team, team_name=request.body.team_name, team_size=request.body.team_size )
    return Response(status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST', ])
def postMentor(request,pk):

    User_instance = User.objects.get( email = request.data['user_email'] )
    ProblemStatement_instance = ProblemStatement.objects.get(pk=pk)
    Mentor.objects.create( mentor= User_instance, problemStatement=ProblemStatement_instance, is_indivisual=request.data['is_indivisual'], organization_name=request.data['organization_name'] )
    # console.log( contestant=request.body.user_email, ProblemStatement=pk, category=request.body.contestant, is_team=request.body.is_team, team_name=request.body.team_name, team_size=request.body.team_size )
    return Response(status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST', ])
def postSponsor(request,pk):

    User_instance = User.objects.get( email = request.data['user_email'] )
    ProblemStatement_instance = ProblemStatement.objects.get(pk=pk)
    Sponsor.objects.create( sponsor= User_instance, problemStatement=ProblemStatement_instance, is_indivisual=request.data['is_indivisual'], organization_name=request.data['organization_name'] )
    # console.log( contestant=request.body.user_email, ProblemStatement=pk, category=request.body.contestant, is_team=request.body.is_team, team_name=request.body.team_name, team_size=request.body.team_size )
    return Response(status=status.HTTP_201_CREATED)
