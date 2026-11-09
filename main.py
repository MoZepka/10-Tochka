from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MOVIES = [
	{
"id": 1, 
"name": "Уличный кот по кличке Боб",
"director": "Роджер Спотисот",
"year": 2016
	},
	{
'id': 2,
"name": "Анора",
"director": "Шон Бейкер",
"year": 2024
	}
	]

app = FastAPI()

class Movie(BaseModel):
	id: int
	name: str
	director: str
	year: int

class MovieCreate(BaseModel):
	name: str = Field(min_length=2)
	director: str = Field(min_length=2)
	year: int = Field(ge=1900, le=2030)

@app.get("/movies", response_model=list[Movie])
def moviesGET():
	return MOVIES

@app.get("/movies/{movie_id}", response_model=Movie)
def movie_idGET(movie_id: int):
	for movie in MOVIES:
		if movie["id"] == movie_id:
			return movie
	raise HTTPException(status_code=404, detail="Movie dosn't find")

@app.post("/movies", response_model=Movie, status_code=201)
def moviePOST(movie: MovieCreate):
	for saved_movie in MOVIES:
		if saved_movie["name"].lower() == movie.name.lower():
			raise HTTPException(status_code=400, detail="Movie with such name have been")
	new_movie = movie.model_dump()
	new_movie["id"] = len(MOVIES) + 1
	MOVIES.append(new_movie)
	return new_movie
