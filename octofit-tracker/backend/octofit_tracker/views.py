from django.shortcuts import render

from .models import Team


def index(request):
    """Renderiza o dashboard com o ranking de equipes.

    Observação: Djongo falha ao traduzir anotations/aggregations complexas
    (ex.: Sum sobre relacionamentos aninhados). Para compatibilidade com
    MongoDB via Djongo, fazemos a agregação em Python:
      - pré-carregamos membros + atividades com prefetch_related
      - somamos `duration_min` em Python e adicionamos `total_minutes`
      - ordenamos o resultado em memória

    Esta abordagem evita a tradução de SQL gerada pelo ORM que causa o
    erro de banco de dados em ambientes MongoDB/Djongo.
    """
    # pré-carrega membros e as atividades relacionadas para evitar N+1
    teams_qs = Team.objects.prefetch_related('members__activities')

    teams = []
    for team in teams_qs:
        total = 0
        # iterar em Python é seguro e evita operações de agregação que o
        # Djongo não consegue traduzir para MongoDB
        for member in team.members.all():
            for act in member.activities.all():
                total += (act.duration_min or 0)
        team.total_minutes = total
        teams.append(team)

    # ordena em memória pelo total calculado
    teams.sort(key=lambda t: t.total_minutes, reverse=True)

    return render(request, 'index.html', {'teams': teams})


def create_activity(request):
    """Form simples para registrar uma nova Activity.

    O formulário permite selecionar `user`, `team` (opcional) e `duration_min`.
    Se a equipe selecionada não contiver o usuário, o usuário será adicionado
    à equipe (comportamento explícito e útil para demo). Após salvar,
    redireciona para a página de ranking (`home`).
    """
    from django import forms
    from django.shortcuts import redirect
    from django.utils import timezone
    from django.contrib.auth import get_user_model
    from .models import Team, Activity

    class _ActivityForm(forms.Form):
        user = forms.ModelChoiceField(get_user_model().objects.all())
        team = forms.ModelChoiceField(Team.objects.all(), required=False)
        activity_type = forms.ChoiceField(choices=Activity.ACTIVITY_CHOICES, initial='workout')
        duration_min = forms.IntegerField(min_value=1)

    if request.method == 'POST':
        form = _ActivityForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            team = form.cleaned_data['team']
            duration = form.cleaned_data['duration_min']
            activity_type = form.cleaned_data['activity_type']

            # se selecionou time e usuário não pertencer, adiciona (convenção de demo)
            if team and not team.members.filter(pk=user.pk).exists():
                team.members.add(user)

            Activity.objects.create(
                user=user,
                activity_type=activity_type,
                duration_min=duration,
                timestamp=timezone.now(),
            )
            return redirect('home')
    else:
        form = _ActivityForm()

    return render(request, 'activity_form.html', {'form': form})
