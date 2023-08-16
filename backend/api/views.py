from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import viewsets, UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.models import Tag, Recipe, Ingredient, FavoritesList, \
    ShoppingList, RecipeIngredient
from users.models import Subscriber
from .filters import RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer, \
    RecipeCreateSerializer, FavoriteOrCartSerializer, CustomUserSerializer, \
    SubscriptionSerializer

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            FavoritesList.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteOrCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            recipe = FavoritesList.objects.filter(user=request.user,
                                                  recipe__id=pk)
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingList.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteOrCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            recipe = ShoppingList.objects.filter(user=request.user,
                                                 recipe__id=pk)
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        shopping_list = 'Необходимые ингредиенты:'
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount'))
        for ingredient in ingredients:
            shopping_list += (
                f"\n- {ingredient['ingredient__name']} "
                f"({ingredient['amount']} "
                f"{ingredient['ingredient__measurement_unit']})")
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="list.txt"'
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            user = request.user
            author = self.get_object()
            Subscriber.objects.create(user=user, author=author)
            serializer = CustomUserSerializer(author,
                                              context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            author = self.get_object()
            subscription = Subscriber.objects.filter(user=user, author=author)
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        subscribed_authors = User.objects.filter(author__user=user)
        pages = self.paginate_queryset(subscribed_authors)
        serializer = SubscriptionSerializer(pages, many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)
