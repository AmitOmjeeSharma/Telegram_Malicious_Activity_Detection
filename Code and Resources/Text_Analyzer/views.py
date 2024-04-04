from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
import os
import joblib

model1 = joblib.load(os.path.dirname(__file__)+ "\\mymodel.pkl")
model2 = joblib.load(os.path.dirname(__file__)+ "\\mySVCModel1.pkl")

# import os
# import pickle
#
# # Specify the path to your .pkl file
# model1 = os.path.join(os.path.dirname(__file__), "\\mymodel.pkl")
# model2 = os.path.join(os.path.dirname(__file__), "\\mySVCModel1.pkl")

# # Load the models
# with open(model1, 'rb') as mymodel.pkl:
#     model1 = pickle.load(mymodel.pkl)
#
# with open(model2, 'rb') as mySVCModel1.pkl:
#     model2 = pickle.load(mySVCModel1.pkl)
#

# Create your views here.
def index(request):
    return render(request, 'index.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def index(request):
#     if (request.method == "POST"):
#         un = request.POST.get('username')
#         up = request.POST.get('password')
#
#         if (un == "DBDA" and up == "DBDA"):
#             request.session['DBDA'] = "DBDA"
#             if (request.session['authdetails'] == "DBDA"):
#                 return render(request, 'index.html')
#             else:
#                 return redirect('/auth')
#         else:
#             return render(request, 'auth.html')
#     else:
#         if (request.session.has_key('authdetails') == True):
#             print("Session Auth")
#             return render(request, 'index.html')
#         else:
#             return render(request, 'auth.html')
#
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkMalicious(request):
    if(request.method == "POST"):
        finalAns = ""
        algo = request.POST.get("algo")
        rawdata = request.POST.get("rawdata")

        if(algo == "Algo-1"):
            finalAns = model1.predict([rawdata])[0]
            #model1.predict([rawdata])[0]
            param = {"answer" : finalAns}
            return render(request, 'output.html', param)
        elif(algo == "Algo-2"):
            finalAns = model2.predict([rawdata])[0]
            #model2.predict([rawdata])[0]
            param = {"answer": finalAns}
            return render(request, 'output.html', param)
        else:
            return redirect('/')
    else:
        return render(request, 'index.html')




# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def logout(request):
#     if(request.session.has_key('authdetails') == True):
#         request.session.clear()
#         print("-----------------")
#         # request.session.flush()
#         return redirect('/')
#     else:
#         return redirect('/')