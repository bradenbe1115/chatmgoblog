from content_index.service_layer import unit_of_work

def bootstrap(uow: unit_of_work.AbstractUnitOfWork = unit_of_work.ChromaDBUnitOfWork()):

    return {"uow": uow}