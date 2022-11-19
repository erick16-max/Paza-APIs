from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Question, Choice, Forum, ForumComment, ForumVote, Profile
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import QuestionSerializer, ChoiceSerializer,ForumCommentSerializer, ForumSerializer, ForumVoteSerializer,UserSerializer, MyTokenObtainPairSerializer, ProfileSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def questions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    if request.method == 'POST':
        user = request.user
        print(user.username)
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def question_detail(request,pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'PUT':
        serializer = QuestionSerializer(question, data=request.data )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def choices(request):
    if request.method == 'GET':
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_choice(request, pk):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=pk)
        user = request.user
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            choice = Choice.objects.filter(user=user, question=question).first()
            if not choice:
                choice = serializer.save(question=question, user=user)
                choice.votes += 1
                choice.save() 
                return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
            else:
                return Response("you already voted", status= status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def forums(request):
 forums = Forum.objects.all()
 selializer = ForumSerializer(forums, many=True)
 return Response(selializer.data)


 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_forum(request):
    selializer = ForumSerializer(data=request.data)
    if selializer.is_valid():
        selializer.save(username=request.user.username)
        return Response(selializer.data, status=status.HTTP_201_CREATED)
    return Response(selializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_forum(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    selializer = ForumSerializer(forum ,data=request.data)
    if selializer.is_valid():
        selializer.save(username=request.username)
        return Response(selializer.data,)
    return Response(selializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_forum(request, pk):
    forum = get_object_or_404(Forum,pk=pk)
    forum.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments(request,pk):
    forum_comment = ForumComment.objects.filter(forum=pk)
    serializer = ForumCommentSerializer(forum_comment, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments_count(request, pk):
    forum_comment = ForumComment.objects.filter(forum=pk)
    # serializer = ForumCommentSerializer(forum_comment, many=True)
    count = forum_comment.count()
    
    return Response(count)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request,pk):
    serializer = ForumCommentSerializer(data=request.data)
    forum = get_object_or_404(Forum, pk=pk)
    if serializer.is_valid():
        serializer.save(username=request.user.username, forum=forum)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def forum_get_votes(request,pk):
    forum_votes = ForumVote.objects.filter(forum=pk)
    serializer = ForumVoteSerializer(forum_votes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_vote(request,pk):
    up_vote = request.data['up_vote']
    down_vote = request.data['down_vote']
    user = request.user
    forum = get_object_or_404(Forum, pk=pk)
    serializer = ForumVoteSerializer(data=request.data)
    
    if serializer.is_valid():
        forum_vote = ForumVote.objects.filter(username=user.username, forum=forum).first()
        if not forum_vote:
            if up_vote == 1 and down_vote == 0:
                vote = serializer.save(username=user.username,forum=forum)
                vote.up_vote + 1
                vote.down_vote + 0
                vote.save()
                return Response(ForumVoteSerializer(vote).data, status=status.HTTP_201_CREATED)

            elif up_vote == 0 and down_vote == 1:
                vote = serializer.save(username=user.username,forum=forum)
                vote.up_vote + 0
                vote.down_vote + 1
                vote.save()
            
                return Response(ForumVoteSerializer(vote).data, status=status.HTTP_201_CREATED)
        else:
            return Response("your vote was already counted", status= status.HTTP_403_FORBIDDEN)
    return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vote_counts(request, pk):
    forum_votes = ForumVote.objects.filter(forum=pk)
    return Response(forum_votes.count())


@api_view(['GET'])
def get_auth_apis(request):
    routes = [
        {
            "method": "GET",
            "url": "api/token/",
            "description": "getting tokens for authentication/logging user"
        },
        {
            "method": "GET",
            "url": "api/token/refresh/",
            "description": "getting refresh token for access"
        },
        {
            "method": "POST",
            "url": "api/signup/",
            "description": "register a user"
        },
        {
            "method": "GET",
            "url": "api/questions/",
            "description": "getting all questions"
        },
        {
            "method": "POST",
            "url": "api/create-question/",
            "description": "creating a question"
        },
        {
            "method": "GET",
            "url": "api/question/<int:pk>/",
            "description": "getting a single question"
        },
        {
            "method": "PUT",
            "url": "api/question/<int:pk>/update",
            "description": "updating a single question"
        },
        {
            "method": "DELETE",
            "url": "api/question/<int:pk>/delete",
            "description": "deleting a single question"
        },
        {
            "method": "GET",
            "url": "api/choices",
            "description": "getting all choices"
        },
        {
            "method": "POST",
            "url": "api/question/<int:pk>/choice/",
            "description": "submitting a choice or answer from a given question"
        },
        
    ]

    return Response(routes)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def create_user(request):
    username = request.data['username']
    email = request.data['email']
    county = request.data['county']
    association = request.data['association']
    password1 = request.data['password1']
    password2 = request.data['password2']
    if password1 == password2:
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        user_profile = Profile.objects.get(user=user)
        user_profile.user = user
        user_profile.county = county
        user_profile.association = association
        user_profile.save()
    else:
        return Response("password do not match")
    return Response("registred")
    










    






        
    

        


