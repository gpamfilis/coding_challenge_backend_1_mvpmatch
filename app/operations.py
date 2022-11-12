from app.errors import ResourceDoesNotExistError, ResourceNotFoundError


def delete_model_operation(model, query, session):
    obj = model.query.filter_by(**query).first()
    if not obj:
        raise ResourceDoesNotExistError()
    session.delete(obj)
    session.commit()


def update_data_operation(model, query, data, session):
    obj = model.query.filter_by(**query).first()
    if not obj:
        raise ResourceNotFoundError("Object does not exist.")
    for key, value in data.items():
        print(key)
        setattr(obj, key, value)
    session.commit()
    return obj
