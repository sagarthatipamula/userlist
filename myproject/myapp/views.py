# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import os
# import pandas as pd
#
#
# def read_excel(search_value, name, staffid_col, user_active_col):
#     folderpath = "Application Files/" + name
#     dirfiles = [f for f in os.listdir(folderpath) if os.path.isfile(os.path.join(folderpath, f))]
#
#     df = pd.DataFrame()
#
#     for file in dirfiles:
#         fname = folderpath + "/" + file
#         df = df._append(pd.read_excel(fname))
#
#     return transform_data(df, search_value, name, staffid_col, user_active_col)
#
#
# def transform_data(df, search_value, name, staffid_col, user_active_col):
#     filtered_df = df.loc[df[staffid_col].str.strip().str.lower() == search_value.strip().lower()].copy()
#
#     if filtered_df.shape[0] > 0:
#         filtered_df.loc[:, 'app_name'] = name
#         filtered_df.loc[:, 'status'] = filtered_df.apply(
#             lambda x: filtered_df[user_active_col] if len(user_active_col) > 0 else "Active", axis=1
#         )
#         filtered_df.loc[:, 'enabled'] = ""  # You can replace this with your logic for 'enabled'
#
#         filtered_df2 = filtered_df[['app_name', 'status', 'enabled']]
#
#         return filtered_df2
#
#     return pd.DataFrame(columns=['app_name', 'status', 'enabled'])
#
#
# x = {
#     "Samplefile1": read_excel,
#     "Samplefile2": read_excel,
#     "Samplefile3": read_excel
# }
#
#
# @csrf_exempt
# def search_data(request, search_value):
#     search_value = search_value.lower()
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     config_file_path = os.path.join(base_dir, 'new_config.json')
#     print("the config file path is", config_file_path)
#     with open(config_file_path) as file:
#         data = json.load(file)
#         print(data)
#
#     result_dataframe = pd.DataFrame(columns=['app_name', 'status'])
#
#     for i in data:
#         result_dataframe = result_dataframe._append(
#             x[i["name"]](search_value, i["name"], i["staffid_col"], i["user_active_col"])
#         )
#
#     response_data = result_dataframe.to_dict(orient='records')
#     return JsonResponse(response_data, safe=False)
from django.http import JsonResponse
import json
import os
import pandas as pd
# views.py (myapp/views.py)
from django.shortcuts import render
from django.shortcuts import render

# views.py

from django.shortcuts import render
from django.http import JsonResponse

#
# def your_view(request, search_value):
#     # Your view logic here
#     # Use the 'search_value' parameter as needed in your view
#     # For example, you can include it in the response
#     response_data = {
#         'search_value': search_value,
#         'message': 'This is your view response.',
#     }
#     return JsonResponse(response_data)


def read_excel(search_value, name, staffid_col, user_active_col):
    folderpath = "Application Files/" + name
    dirfiles = [f for f in os.listdir(folderpath) if os.path.isfile(os.path.join(folderpath, f))]

    df = pd.DataFrame()

    for file in dirfiles:
        fname = folderpath + "/" + file
        df = df._append(pd.read_excel(fname))

    return transform_data(df, search_value, name, staffid_col, user_active_col)


def transform_data(df, search_value, name, staffid_col, user_active_col):
    filtered_df = df.loc[df[staffid_col].str.strip().str.lower() == search_value.strip().lower()].copy()

    if filtered_df.shape[0] > 0:
        filtered_df.loc[:, 'app_name'] = name
        filtered_df.loc[:, 'status'] = filtered_df.apply(
            lambda x: filtered_df[user_active_col] if len(user_active_col) > 0 else "Active", axis=1
        )
        filtered_df.loc[:, 'enabled'] = ""  # You can replace this with your logic for 'enabled'

        filtered_df2 = filtered_df[['app_name', 'status', 'enabled']]

        return filtered_df2

    return pd.DataFrame(columns=['app_name', 'status', 'enabled'])


x = {
    "Samplefile1": read_excel,
    "Samplefile2": read_excel,
    "Samplefile3": read_excel
}


def search_api(request, search_value):
    search_value = search_value.lower()

    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_file_path = os.path.join(base_dir, 'new_config.json')

        with open(config_file_path) as file:
            data = json.load(file)

        result_dataframe = pd.DataFrame(columns=['app_name', 'status'])

        for i in data:
            result_dataframe = result_dataframe._append(
                x[i["name"]](search_value, i["name"], i["staffid_col"], i["user_active_col"])
            )

        response_data = result_dataframe.to_dict(orient='records')
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return JsonResponse({"error": error_message}, status=500)



def show_search_page(request):
    return render(request, 'myapp/search_page.html')
