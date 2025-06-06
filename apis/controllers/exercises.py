from django.shortcuts import get_object_or_404
from ninja import PatchDict, Query
from ninja_extra import ControllerBase, api_controller, route

from core.throttle import BurstRateThrottle

from ..models.exercises import Exercise as exerciseModel
from ..models.schemas.exercises import *
from ..models.schemas.exercises import _ExerciseFilter
from core.exceptions import *
from core.authentications.ninja import GlobalAuth


@api_controller("exercise/", auth=GlobalAuth(), tags=["Exercise"], permissions=[])
class ExerciseController(ControllerBase):
    @route.get(
        "/list", response={200: list[Exercise], 404: Error}, permissions=[], throttle=[BurstRateThrottle()]
    )  # noqa: UP006
    def get_exercises(self, filters: _ExerciseFilter = Query(None)):  # noqa: B008
        """
        Get a list of exercises with optional filtering.
        """
        queryset = exerciseModel.objects.all()
        print(queryset)
        if filters:
            # queryset = queryset.filter(**filters)
            queryset = filters.filter(queryset) if filters else queryset
        return list(queryset)

    @route.put("/bulk", response={200: list[Exercise]}, permissions=[])  # noqa: UP006
    def bulk_create_exercises(self, request, payload: list[PatchDict[PatchExercise]]):  # noqa: B008, UP006
        """
        bulk Creation of Exercises.
        """
        exercises = []
        for item in payload:
            exercise = exerciseModel()
            for attr, value in item.items():
                setattr(exercise, attr, value)
            exercise.save()
            exercises.append(exercise)
        return exercises

    @route.post("/create", response={201: Exercise}, permissions=[])  # noqa: UP006
    def create_exercise(self, request, payload: PatchDict[PatchExercise]):  # noqa: B008
        """
        Create a new exercise.
        """
        obj = exerciseModel()
        for attr, value in payload.items():
            setattr(obj, attr, value)

        obj.save()

        return 201, obj

    @route.get("/get/{exercise_id}", response={200: Exercise, 404: Error}, permissions=[])  # noqa: UP006
    def get_exercise(self, request, exercise_id: int):
        """
        Get a specific exercise by ID.
        """
        exercise = get_object_or_404(exerciseModel, id=exercise_id)
        if exercise:
            return 200, exercise
        else:
            return 404, {"message": "exercise not found"}

    @route.get("/get_profile/{profile_id}", response={200: Exercise}, permissions=[])  # noqa: UP006
    def get_exercise_profile(self, request, profile_id: int):
        """
        Get a specific exercise by ID.
        """
        exercise = exerciseModel.objects.get_by_profile(profile_id=profile_id)
        if exercise:
            return 200, exercise
        else:
            return 404, {"message": "profile not found"}

    @route.patch("/update/{exercise_id}", response={200: Exercise}, permissions=[])  # noqa: UP006
    def update_exercise(self, request, exercise_id: int, payload: PatchDict[PatchExercise]):
        """
        Update an existing exercise by ID.
        """
        exercise = get_object_or_404(exerciseModel, id=exercise_id)
        print(payload.values())
        for attr, value in payload.items():
            setattr(exercise, attr, value)

        exercise.save()
        return exercise

    @route.delete("/delete/{exercise_id}", response={204: None}, permissions=[])  # noqa: UP006
    def delete_exercise(self, request, exercise_id: int):
        """
        Delete an exercise by ID.
        """
        exercise = get_object_or_404(exerciseModel, id=exercise_id)
        exercise.delete()
        return 204, None
