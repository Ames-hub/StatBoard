from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
try:
    # This is to prevent an error when running "python webui/manage.py migrate" command
    from database import db
except ModuleNotFoundError:
    pass
import sqlite3
import json

def targetted_fetch_stats(target_name):
    if target_name is None or target_name == "":
        return {"error": "A statistic name is required to fetch stats."}

    stats_data = db.get_statistics(target_name, searchback=7)
    return {"stats": stats_data}

def indiscriminate_fetch_stats():
    """
    Fetches all statistics from the database. More or less an alias for db.get_statistics("*")
    :return:
    """
    stats_data = db.get_statistics(stat_name="*", searchback=7)
    return {"stats": stats_data}

# noinspection PyUnusedLocal
class views:
    @staticmethod
    def dashboard(request):
        return render(request, 'dashboard.html')

    @staticmethod
    def statsboard(request):
        return render(request, 'statsboard.html')

    @staticmethod
    def ping(request):
        data = {"msg": "ok"}  # If it could receive the request, it means the server is up
        return JsonResponse(data)

    @staticmethod
    def getstats(request):
        target_name = request.GET.get('target_name', None)
        if not type(target_name) is str:
            return JsonResponse({"error": "target_name must be a string"}, status=400)
        else:
            target_name = target_name.strip()

        if target_name is None or target_name == "":
            return JsonResponse({"error": "target_name is required"}, status=400)

        if target_name == "*":
            stats_data = indiscriminate_fetch_stats()
        else:
            stats_data = targetted_fetch_stats(target_name)

        return JsonResponse(stats_data)

    @staticmethod
    def add_statistic_page(request):
        return render(request, 'stats/add.html')

    @staticmethod
    def delete_statistic_page(request):
        return render(request, 'stats/delete.html')

    # TODO: Implement this method (eventually)
    @staticmethod
    def view_target_stats(request, target_name):
        raise NotImplementedError("This method is not yet implemented")

    @staticmethod
    def create_new_statistic(request):
        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=405)

        try:
            # Parse the JSON data from request.body
            data = json.loads(request.body)
            stat_name = data.get('stat_name')
            stat_desc = data.get('stat_desc')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        if not isinstance(stat_name, str) or not stat_name.strip():
            return JsonResponse({"error": "A valid statistic name is required"}, status=400)

        stat_name = stat_name.strip()

        if stat_desc is not None:
            if not isinstance(stat_desc, str):
                return JsonResponse({"error": "Statistic description must be a text string"}, status=400)
            stat_desc = stat_desc.strip()
        else:
            stat_desc = None

        # Assuming db.enter_new_stat is a function that saves the new statistic to the database
        try:
            db.track_new_stat(stat_name, stat_desc)
        except sqlite3.IntegrityError:
            return JsonResponse({"error": "Statistic already exists!"}, status=400)
        return JsonResponse({"msg": "ok"})

    @staticmethod
    def delete_statistic(request):
        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=405)

        try:
            # Parse the JSON data from request.body
            data = json.loads(request.body)
            stat_name = data.get('stat_name')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        if not isinstance(stat_name, str) or not stat_name.strip():
            return JsonResponse({"error": "A valid statistic name is required"}, status=400)

        stat_name = stat_name.strip()

        # Assuming db.delete_stat is a function that deletes the statistic from the database
        try:
            db.delete_tracked_stat(stat_name)
        except sqlite3.IntegrityError:
            return JsonResponse({"error": "Statistic does not exist!"}, status=400)
        return JsonResponse({"msg": "ok"})

    @staticmethod
    def enter_stat_data(request):
        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=405)

        try:
            # Parse the JSON data from request.body
            data = json.loads(request.body)
            stat_name = data.get('target')
            value = data.get('value')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        if type(stat_name) is not str:
            return JsonResponse({"error": "A statistic name type as string is required"}, status=400)

        stat_name = stat_name.strip()

        if not all(letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789_-" for letter in stat_name):
            return JsonResponse({"error": "A valid statistic name is required"}, status=400)

        # Checks the stat name exists in the database
        if not db.check_stat_exists(stat_name):
            return JsonResponse({"error": "That statistic does not exist!"}, status=400)

        stat_name = stat_name.strip()

        try:
            value = int(value)
        except ValueError:
            return JsonResponse({"error": "Value must be an integer"}, status=400)

        # Assuming db.enter_stat_data is a function that saves the new statistic data to the database
        try:
            db.enter_stat_data(stat_name, value)
        except sqlite3.IntegrityError:
            return JsonResponse({"error": "Statistic does not exist!"}, status=400)

        return JsonResponse({"msg": "ok"})

    @staticmethod
    def delete_stat_data(request):
        """
        Deletes a statistic data point from the database for a certain date and statistic name
        :param request:
        :return:
        """
        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=405)

        try:
            # Parse the JSON data from request.body
            data = json.loads(request.body)
            stat_name = data.get('target')
            date = data.get('date')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        if not isinstance(stat_name, str) or not stat_name.strip():
            return JsonResponse({"error": "A valid statistic name is required"}, status=400)

        if not isinstance(date, str) or not date.strip():
            return JsonResponse({"error": "A valid date is required"}, status=400)

        stat_name = stat_name.strip()
        date = date.strip()

        # Assume we get the date in the format YYYY-MM-DD, reformat to datetime.date
        date = datetime.strptime(date, '%Y-%m-%d').date()

        # Assuming db.delete_stat_data is a function that deletes the statistic data from the database
        try:
            db.delete_stat_data(stat_name, date)
        except sqlite3.IntegrityError:
            return JsonResponse({"error": "Statistic does not exist!"}, status=400)
        return JsonResponse({"msg": "ok"})