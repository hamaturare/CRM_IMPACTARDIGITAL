from django.shortcuts import render, redirect, get_object_or_404
from apps.visualadmin.models import ChatbotState, ChatbotQuestion, ChatbotOption
from django.contrib.auth.decorators import login_required

@login_required
def visualadmin(request):
    if request.method == 'POST':
        # Handle form submissions to add or edit states, questions, and options
        if 'add_state' in request.POST:
            state_name = request.POST.get('state_name')
            if state_name:
                ChatbotState.objects.create(name=state_name)
        elif 'edit_state' in request.POST:
            state_id = request.POST.get('state_id')
            state_name = request.POST.get('state_name')
            state = get_object_or_404(ChatbotState, id=state_id)
            state.name = state_name
            state.save()
        elif 'add_question' in request.POST:
            state_id = request.POST.get('state_id')
            question_text = request.POST.get('question_text')
            question_type = request.POST.get('question_type')
            invalid_response_message = request.POST.get('invalid_response_message')
            custom_field_name = request.POST.get('custom_field_name')
            state = get_object_or_404(ChatbotState, id=state_id)
            ChatbotQuestion.objects.create(
                state=state,
                question_text=question_text,
                question_type=question_type,
                invalid_response_message=invalid_response_message,
                custom_field_name=custom_field_name
            )
        elif 'edit_question' in request.POST:
            question_id = request.POST.get('question_id')
            question_text = request.POST.get('question_text')
            question_type = request.POST.get('question_type')
            invalid_response_message = request.POST.get('invalid_response_message')
            custom_field_name = request.POST.get('custom_field_name')
            question = get_object_or_404(ChatbotQuestion, id=question_id)
            question.question_text = question_text
            question.question_type = question_type
            question.invalid_response_message = invalid_response_message
            question.custom_field_name = custom_field_name
            question.save()
        elif 'add_option' in request.POST:
            question_id = request.POST.get('question_id')
            option_text = request.POST.get('option_text')
            response_message = request.POST.get('response_message')
            next_state_id = request.POST.get('next_state_id')
            question = get_object_or_404(ChatbotQuestion, id=question_id)
            next_state = get_object_or_404(ChatbotState, id=next_state_id) if next_state_id else None
            ChatbotOption.objects.create(
                question=question,
                option_text=option_text,
                response_message=response_message,
                next_state=next_state
            )
        elif 'edit_option' in request.POST:
            option_id = request.POST.get('option_id')
            option_text = request.POST.get('option_text')
            response_message = request.POST.get('response_message')
            next_state_id = request.POST.get('next_state_id')
            option = get_object_or_404(ChatbotOption, id=option_id)
            option.option_text = option_text
            option.response_message = response_message
            option.next_state = get_object_or_404(ChatbotState, id=next_state_id) if next_state_id else None
            option.save()
        elif 'delete_state' in request.POST:
            state_id = request.POST.get('state_id')
            state = get_object_or_404(ChatbotState, id=state_id)
            state.delete()
        elif 'delete_question' in request.POST:
            question_id = request.POST.get('question_id')
            question = get_object_or_404(ChatbotQuestion, id=question_id)
            question.delete()
        elif 'delete_option' in request.POST:
            option_id = request.POST.get('option_id')
            option = get_object_or_404(ChatbotOption, id=option_id)
            option.delete()
        return redirect('visualadmin')

    states = ChatbotState.objects.all()
    return render(request, 'visualadmin/visualadmin.html', {'states': states})

@login_required
def add_state(request):
    state_name = request.POST.get('state_name')
    if state_name:
        ChatbotState.objects.create(name=state_name)
    return redirect('visualadmin')

@login_required
def edit_state(request):
    state_id = request.POST.get('state_id')
    state_name = request.POST.get('state_name')
    state = get_object_or_404(ChatbotState, id=state_id)
    state.name = state_name
    state.save()
    return redirect('visualadmin')

@login_required
def delete_state(request):
    state_id = request.POST.get('state_id')
    state = get_object_or_404(ChatbotState, id=state_id)
    state.delete()
    return redirect('visualadmin')

@login_required
def add_question(request):
    state_id = request.POST.get('state_id')
    question_text = request.POST.get('question_text')
    question_type = request.POST.get('question_type')
    invalid_response_message = request.POST.get('invalid_response_message')
    custom_field_name = request.POST.get('custom_field_name')
    state = get_object_or_404(ChatbotState, id=state_id)
    ChatbotQuestion.objects.create(
        state=state,
        question_text=question_text,
        question_type=question_type,
        invalid_response_message=invalid_response_message,
        custom_field_name=custom_field_name
    )
    return redirect('visualadmin')

@login_required
def edit_question(request):
    question_id = request.POST.get('question_id')
    question_text = request.POST.get('question_text')
    question_type = request.POST.get('question_type')
    invalid_response_message = request.POST.get('invalid_response_message')
    custom_field_name = request.POST.get('custom_field_name')
    question = get_object_or_404(ChatbotQuestion, id=question_id)
    question.question_text = question_text
    question.question_type = question_type
    question.invalid_response_message = invalid_response_message
    question.custom_field_name = custom_field_name
    question.save()
    return redirect('visualadmin')

@login_required
def delete_question(request):
    question_id = request.POST.get('question_id')
    question = get_object_or_404(ChatbotQuestion, id=question_id)
    question.delete()
    return redirect('visualadmin')

@login_required
def add_option(request):
    question_id = request.POST.get('question_id')
    option_text = request.POST.get('option_text')
    response_message = request.POST.get('response_message')
    next_state_id = request.POST.get('next_state_id')
    question = get_object_or_404(ChatbotQuestion, id=question_id)
    next_state = get_object_or_404(ChatbotState, id=next_state_id) if next_state_id else None
    ChatbotOption.objects.create(
        question=question,
        option_text=option_text,
        response_message=response_message,
        next_state=next_state
    )
    return redirect('visualadmin')

@login_required
def edit_option(request):
    option_id = request.POST.get('option_id')
    option_text = request.POST.get('option_text')
    response_message = request.POST.get('response_message')
    next_state_id = request.POST.get('next_state_id')
    option = get_object_or_404(ChatbotOption, id=option_id)
    option.option_text = option_text
    option.response_message = response_message
    option.next_state = get_object_or_404(ChatbotState, id=next_state_id) if next_state_id else None
    option.save()
    return redirect('visualadmin')

@login_required
def delete_option(request):
    option_id = request.POST.get('option_id')
    option = get_object_or_404(ChatbotOption, id=option_id)
    option.delete()
    return redirect('visualadmin')
