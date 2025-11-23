class User:
    def __init__(self,id,full_name,email,join_date):
        self.id=id
        self.full_name=full_name
        self.email=email
        self.join_date=join_date

    def __str__(self):
        return f"id: {self.id}, full_name: {self.full_name} email: {self.email} join_date: {self.join_date}"
    

class Exercise:
    def __init__(self,id,name,muscle_group):
        self.id=id
        self.name=name
        self.muscle_group=muscle_group


class WorkoutExercise:
    def __init__(self,exercise:Exercise,sets:int, reps:int, weight :float):
        self.exercise=exercise
        self.sets=sets
        self.reps=reps
        self.weight=weight

    def total_volume(self):
        return self.sets * self.reps * self.weight


class Workout:
    def __init__(self,id ,user,date ,notes  ):
        self.id=id
        self.user=user
        self.date=date
        self.notes=notes
        self.exercises:list[WorkoutExercise]=[]

    def add_exercise(self, workout_exercise):
        self.exercises.append(workout_exercise)

    
    def total_workout_volume(self):
        total = 0
        for we in self.exercises:
            total += we.total_volume()   
        return total
    
