from rest_framework import generics, permissions , status
from .models import Article , Favoris, Comment, Like
from .serializers import ArticleSerializer , FavoriteSerializer,CommentSerializer, LikeSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ArticleFilter


#pour Afficher la liste des articles 
class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []

#pour ajouter un articles 
class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

#pour recuperer un article (afficher un article )
class ArticleRetrieveView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []

#1 ajouter des condition de permission et que l'auteur de l'article est le seule qui peut acceder a ces fonctionnalité 
class IsArticleOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the authenticated user is the owner of the article
        return obj.auteur == request.user
    
#pour modifier ou supprimer un article 
class ArticleUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated,IsArticleOwner]


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

###comments and likes 

class CommentDestroyView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(user=user)


class LikeView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.get_serializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        article_id = self.kwargs['pk']
        return Article.objects.get(pk=article_id)

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(user=user, article=article)

        if not created:
            like.delete()
            message = 'Like removed.'
        else:
            message = 'Like added.'

        serializer = self.get_serializer(article)
        return Response({'article': serializer.data, 'message': message}, status=status.HTTP_200_OK)


###########################################################################################"
#favoris :

#ajouter article au favoris 
class FavoriteCreateView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        article_id = kwargs.get('pk')
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favoris.objects.get_or_create(user=request.user, article=article)

        if created:
            serializer = self.get_serializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Article already added to favorites'}, status=status.HTTP_400_BAD_REQUEST)

#afficher Liste des favoris 
class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favoris.objects.filter(user=self.request.user)

 ###############################################################################
 #filtrage et rechercher des articles 
class ArticleSearchListAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ArticleFilter
    search_fields = ['nom_article', 'description']
    pagination_class = None
    permission_classes = []