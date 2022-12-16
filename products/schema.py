import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from . models import Category, Book, Grocery, Author, Ingredient


class CategoryType(DjangoObjectType):

    class Meta:
        model = Category

        filter_fields = ['title', 'ingredients']
        interfaces = (relay.Node, )


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class GroceryType(DjangoObjectType):
    class Meta:
        model = Grocery


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__title': ['exact'],
        }
        interfaces = (relay.Node, )


class UpdateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    def mutate(self, info, title, id):
        category = Category.objects.get(id=id)
        category.title = title
        category.save()
        return UpdateCategory(title=title, id=id)


class CreateIngredent(graphene.Mutation):
    ingredients = graphene.Field(IngredientType())

    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String()
        category = graphene.ID()

    def mutate(self, info,  notes, name, category):
        cat = Ingredient(name=name, notes=notes, category=category)
        cat.save()

        return CreateIngredent(ingredients=cat)


class CreateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        title = graphene.String()

    def mutate(self, info, title):
        cat = Category(title=title)
        # category.title = title
        cat.save()
        return CreateCategory(category=cat)


class BookInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    author = graphene.String(required=True)
    pages = graphene.Int()
    price = graphene.Int()
    quantity = graphene.Int()
    description = graphene.String()
    status = graphene.String()


class CreateBook(graphene.Mutation):
    class Arguments:
        input = BookInput(required=True)

    Fieldbook = graphene.Field(BookType)

    def mutate(self, info, input):
        book = Book()
        book.title = input.title
        book.author = input.author
        book.pages = input.pages
        book.price = input.price
        book.quantity = input.quantity
        book.description = input.description
        book.status = input.status
        book.save()
        return CreateBook(Fieldbook=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        # book = graphene.Field(BookType)
        input = BookInput(required=True)
        id = graphene.ID()

    book = graphene.Field(BookType)

    def mutate(cls, root, info, input, id):
        book = Book.objects.get(pk=id)
        book.title = input.title
        book.author = input.author
        book.pages = input.pages
        book.price = input.price
        book.quantity = input.quantity
        book.description = input.description
        book.status = input.status
        book.save()
        return UpdateBook(book=book)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    create_ingrdent = CreateIngredent.Field()


class Query(object):
    all_categories = graphene.List(CategoryType)
    all_books = graphene.List(BookType)
    all_author = graphene.List(AuthorType)
    all_groceries = graphene.List(GroceryType)
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(
        CategoryType, title=graphene.String(required=True))
    category = relay.Node.Field(CategoryType)
    all_categories_filter = DjangoFilterConnectionField(CategoryType)

    ingredient = relay.Node.Field(IngredientType)
    all_ingredients_filter = DjangoFilterConnectionField(IngredientType)
    book_by_id = graphene.Field(BookType, id=graphene.Int())

    def resolve_book_by_id(root, info, id):
        return Book.objects.all()

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, title):
        try:
            return Category.objects.get(title=title)
        except Category.DoesNotExist:
            return None

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_(self, info):
        return Category.objects.all()

    def resolve_all_books(self, info):
        return Book.objects.all()

    def resolve_all_author(self, info):
        return Author.objects.all()

    def resolve_all_groceries(self, info):
        return Grocery.objects.all()
