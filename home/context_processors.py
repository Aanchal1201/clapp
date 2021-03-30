from .models import UserProfile
from quiz.models import Language
def profile(request):
    if not request.user.is_authenticated:
        return { 
            'profile': 'Anonymous'
        }
    else:
        return{
        'profile': UserProfile.objects.filter(UserUsername=request.user).first()
        }

def language(request):
    return {
        'language' : Language.objects.all()
    }