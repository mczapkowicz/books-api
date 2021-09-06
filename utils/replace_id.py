def replace_id(obj):
  if obj.get('_id'):
    id = str(obj.get('_id'))
    del obj['_id']
    obj['id'] = id

  return obj