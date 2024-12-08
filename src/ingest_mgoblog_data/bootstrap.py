from ingest_mgoblog_data.service_layer import unit_of_work

def bootstrap(uow: unit_of_work.AbstractUnitOfWork = unit_of_work.PymongoUnitOfWork()):

    return {"uow": uow}