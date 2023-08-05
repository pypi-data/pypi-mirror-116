from saleboxdjango.models import ContentPage


def sync_contentpage(data):
    # get fieldname
    fieldnames = [f.name for f in ContentPage._meta.get_fields()]

    # retrieve / create object
    o = ContentPage.objects.filter(id=data['id']).first()
    if o is None:
        o = ContentPage()

    # populate foreign keys
    if data['parent']:
        data['parent'] = ContentPage.objects.get(id=data['parent'])

    # save data
    for key in data:
        if key in fieldnames:
            setattr(o, key, data[key])
    o.save()