from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.

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
                }}}})
        context['symptom_list'] = res['hits']['hits']
    if symp_check:
        context['symptom_checked'] = 'on'
        res = es.search(index="disease",
                             body={"query": {
                                 "match_phrase": {
                                     "symptoms": {
                                         "query": query,
                                         "slop": 50
                                     }}}})
        context['symptom_list'] = res['hits']['hits']
    return render(request, 'index.html', context)

def index(request):
    context = {"filter[name]" : "False", "filter[symptom]" : "False"}
    return render(request, 'index.html', context)