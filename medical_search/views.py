from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

def search(request):
    es = Elasticsearch()
    query = request.POST.get('query', None)
    name_check = request.POST.get('filter[name]', None)
    symp_check = request.POST.get('filter[symptom]', None)
    context = {}
    if name_check:
        context['name_checked'] = 'on'
        res = es.search(index="disease", body={"query": {
            "match_phrase": {
                "title": {
                    "query": query,
                    "slop": 50
                }}}}, size=1000)
        lst = res['hits']['hits']
        name_list = {}
        for d in lst:
            name_list[d['_source']['title']] = d['_id']
            #symp_list.append(d['_source']['symptoms'])
        if len(name_list) > 0:
            context['name_list'] = name_list
    if symp_check:
        context['symptom_checked'] = 'on'
        res = es.search(index="disease",
                             body={"query": {
                                 "match_phrase": {
                                     "symptoms": {
                                         "query": query,
                                         "slop": 50
                                     }}}}, size=1000)
        lst = res['hits']['hits']
        symp_list = {}
        for d in lst:
            symp_list[d['_source']['title']] = d['_id']
            #symp_list.append(d['_source']['symptoms'])
        if len(symp_list) > 0:
            context['symp_list'] = symp_list

    return render(request, 'index.html', context)

def result(request, id):
    es = Elasticsearch()
    res = es.get('disease', id=id)
    context={}
    context['title'] = res['_source']['title']
    context['content'] = res['_source']['html']
    return render(request, 'result_page.html', context)

def index(request):
    context = {"filter[name]" : False, "filter[symptom]" : False}
    return render(request, 'index.html', context)