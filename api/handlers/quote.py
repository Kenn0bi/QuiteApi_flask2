from api import app, db, request, multi_auth
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.quote import quote_schema, quotes_schema


@app.route('/quotes', methods=["GET"])
def get_quotes():
    quotes = QuoteModel.query.all()
    return quotes_schema.dump(quotes), 200


@app.route('/quotes/<int:quote_id>', methods=["GET"])
def get_quotes_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        return quote_schema.dump(quote), 200
    return {"Error": f"Quote id={quote_id} not found"}, 404


@app.route('/authors/<int:author_id>/quotes', methods=["GET"])
def get_quotes_by_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404

    quotes = author.quotes.all()
    if quotes:
        return quotes_schema.dump(quotes), 200  # Возвращаем все цитаты автора
    return {"Error": "Quote not found"}, 404


@app.route('/authors/<int:author_id>/quotes', methods=["POST"])
@multi_auth.login_required
def create_quote(author_id):
    # print("user = ", auth.current_user())
    quote_data = request.json
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404

    quote = QuoteModel(author, quote_data["text"])
    db.session.add(quote)
    db.session.commit()
    return quote_schema.dump(quote), 201

@app.route('/quotes/<int:quote_id>', methods=["PUT"])
def edit_quote(quote_id):
    quote_data = request.json
    quote = QuoteModel.query.get(quote_id)
    quote.text = quote_data["text"]
    db.session.commit()
    return quote_schema.dump(quote), 200


@app.route('/quotes/<int:quote_id>', methods=["DELETE"])
def delete_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        db.session.delete(quote)
        db.session.commit()
        return '', 200
    return {"Error": f"Quote id={quote_id} not found"}, 404