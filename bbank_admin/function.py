def handle_uploded_file(f):
    with open("bbank_admin/static/img/" + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
