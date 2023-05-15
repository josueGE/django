from django.contrib.auth.models import User
from rest_framework import serializers, validators

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('username','password','email')
        extra_kwargs = {
            "password":{"write_only":True},
            "email":{
                "required": True,
                "allow_blank":False,
                "validators":[
                    validators.UniqueValidator(
                        User.objects.all(),"ya se registro el email intente con otro")
                ]
            }
        }
    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email=validated_data.get('email')
        # nombre=validated_data.get('nombre')
        # apellido=validated_data.get('apellido')
        user=User.objects.create(
            username=username,
            password=password,
            email=email,
            # nombre=nombre,
            # apellido=apellido
        )
        user.set_password(password)
        user.save()
        return user
        