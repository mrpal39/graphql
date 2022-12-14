import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from . models import *


class CategoryType(DjangoObjectType):

    class Meta:
        model = Category
        fields = ('id', 'title')


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'isbn',
            'pages',
            'price',
            'quantity',
            'description',
            'status',
            'date_created',
        )


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = (
            'id',
            'name',
        )


class GroceryType(DjangoObjectType):
    class Meta:
        model = Grocery
        fields = (
            'product_tag',
            'name',
            'category',
            'price',
            'quantity',
            'imageurl',
            'status',
            'date_created',
        )


class UpdateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(self, info, title, id):
        category = Category.objects.get(id=id)
        category.title = title
        category.save()
        return UpdateCategory(title=title, id=id)


class CreateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        title = graphene.String()

    @classmethod
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

    book = graphene.Field(BookType)

    @classmethod
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
        return CreateBook(Book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        # book = graphene.Field(BookType)
        input = BookInput(required=True)
        id = graphene.ID()

    book = graphene.Field(BookType)

    @classmethod
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


class Query(object):
    categories = graphene.List(CategoryType)
    books = graphene.List(BookType)
    author = graphene.List(AuthorType)
    groceries = graphene.List(GroceryType)

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_books(self, info):
        return Book.objects.all()

    def resolve_all_author(self, info):
        return Author.objects.all()

    def resolve_all_groceries(self, info):
        return Grocery.objects.all()
