import graphene
from graphene_django.types import DjangoObjectType

from recipes.models import Recipe

class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe

class Query(graphene.ObjectType):
    # Opération de visualisation (Lister toutes les recettes)
    all_recipes = graphene.List(RecipeType)
    recipe_by_ingredient = graphene.List(RecipeType, ingredient=graphene.String())
    recipe_by_name = graphene.List(RecipeType, name=graphene.String())

    def resolve_all_recipes(self, info, **kwargs):
        return Recipe.objects.all()
    

    def resolve_all_recipes(self, info, **kwargs):
        return Recipe.objects.all()

    def resolve_recipe_by_ingredient(self, info, ingredient):
        return Recipe.objects.filter(ingredients__icontains=ingredient)

    def resolve_recipe_by_name(self, info, name):
        return Recipe.objects.filter(name__icontains=name)

class CreateRecipe(graphene.Mutation):
    # Input pour la création d'une recette
    class Arguments:
        name = graphene.String(required=True)
        ingredients = graphene.String(required=True)
        instructions = graphene.String(required=True)

    # Résultat de la création
    recipe = graphene.Field(RecipeType)

    def mutate(self, info, name, ingredients, instructions, photo=None):
        recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions, photo=photo)
        recipe.save()
        return CreateRecipe(recipe=recipe)

class UpdateRecipe(graphene.Mutation):
    # Input pour la mise à jour d'une recette
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        ingredients = graphene.String()
        instructions = graphene.String()

    # Résultat de la mise à jour
    recipe = graphene.Field(RecipeType)

    def mutate(self, info, id, **kwargs):
        recipe = Recipe.objects.get(pk=id)
        for field, value in kwargs.items():
            setattr(recipe, field, value)
        recipe.save()
        return UpdateRecipe(recipe=recipe)

class DeleteRecipe(graphene.Mutation):
    # Input pour la suppression d'une recette
    class Arguments:
        id = graphene.ID(required=True)

    # Résultat de la suppression
    ok = graphene.Boolean()

    def mutate(self, info, id):
        recipe = Recipe.objects.get(pk=id)
        recipe.delete()
        return DeleteRecipe(ok=True)

class Mutation(graphene.ObjectType):
    # Opérations de modification (Ajouter, Modifier, Supprimer)
    create_recipe = CreateRecipe.Field()
    update_recipe = UpdateRecipe.Field()
    delete_recipe = DeleteRecipe.Field()

# Schéma global
schema = graphene.Schema(query=Query, mutation=Mutation)