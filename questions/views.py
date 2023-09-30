from django.shortcuts import render, redirect

from questions.forms import QuestionForm, AnswerForm, SearchForm, TagForm
from questions.models import Question, Answer, Tag
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy("users:login"))
def question_detail_view(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = question.answer_set.all()
    answer_form = AnswerForm()

    context = {
        "question": question,
        "answers": answers,
        "answer_form": answer_form
    }
    return render(request, "question/question_detail_view.html", context)


@login_required(login_url=reverse_lazy("users:login"))
def question_list_view(request):
    questions = Question.objects.all()

    return render(request, "question/question_list_view.html", {"questions": questions})


@login_required(login_url=reverse_lazy("users:login"))
def question_update_view(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
        return redirect("questions:question_detail", question_id=question.id)
    else:
        form = QuestionForm()

    return render(request, "question/question_form.html", {"form": form})


@login_required(login_url=reverse_lazy("users:login"))
def question_delete_view(request, question_id):
    Question.objects.get(id=question_id).delete()
    return redirect("questions:question_list")


@login_required(login_url=reverse_lazy("users:login"))
def question_upvote_view(request, question_id):
    question = Question.objects.get(id=question_id)
    user_upvoted_question = question.upvoters.filter(id=request.user.id).exists()
    if not user_upvoted_question:
        question.upvoters.add(request.user)

    return redirect("questions:question_detail", question_id=question_id)


@login_required(login_url=reverse_lazy("users:login"))
def question_downvote_view(request, question_id):
    question = Question.objects.get(id=question_id)
    user_downvoted_question = question.downvoters.filter(id=request.user.id).exists()
    if not user_downvoted_question:
        question.downvoters.add(request.user)

    return redirect("questions:question_detail", question_id=question_id)


@login_required(login_url=reverse_lazy("users:login"))
def question_create_view(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
    else:
        form = QuestionForm()
    return render(request, "question/question_form.html", {"form": form})


@login_required(login_url=reverse_lazy("users:login"))
def question_search_view(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        question_title = request.POST["query"]
        questions = Question.objects.filter(title__contains=question_title)
    else:
        form = SearchForm()
        questions = ""

    context = {
        "form": form,
        "questions": questions
    }

    return render(request, "question/question_search.html", context)


@login_required(login_url=reverse_lazy("users:login"))
def answer_create_view(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
        return redirect("questions:question_detail", question_id=question_id)


@login_required(login_url=reverse_lazy("users:login"))
def answer_update_view(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    question_id = answer.question.id
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer.save()
        return redirect("questions:question_detail", question_id=question_id)
    else:
        form = AnswerForm()

    return render(request, "question/answer_update.html", {"form": form})


@login_required(login_url=reverse_lazy("users:login"))
def answer_delete_view(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    question_id = answer.question.id
    answer.delete()
    return redirect("questions:question_detail", question_id=question_id)


@login_required(login_url=reverse_lazy("users:login"))
def answer_upvote_view(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    question_id = answer.question.id
    user_upvoted_answer = answer.upvoters.filter(id=request.user.id).exists()
    if not user_upvoted_answer:
        answer.upvoters.add(request.user)
    return redirect("questions:question_detail", question_id=question_id)


@login_required(login_url=reverse_lazy("users:login"))
def answer_downvote_view(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    question_id = answer.question.id
    user_downvoted_answer = answer.downvoters.filter(id=request.user.id).exists()
    if not user_downvoted_answer:
        answer.downvoters.add(request.user)
    return redirect("questions:question_detail", question_id=question_id)


@login_required(login_url=reverse_lazy("users:login"))
def tag_list_view(request):
    tags = Tag.objects.all()
    return render(request, "tag/tag_list_view.html", {"tags": tags})


@login_required(login_url=reverse_lazy("users:login"))
def tag_create_view(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TagForm()

    return render(request, "tag/create_tag_form.html", {"form": form})
