from dataclass.container import ContainerRegistry

# Variaveis
username  = 'leticiacb1'
repository_name = 'aps3-mlops-' + username

try: 
    # Instances
    ecr = ContainerRegistry()
    # Create ECR
    ecr.create_client()
    ecr.create_repository(repository_name= repository_name)
except Exception as e:
    print(f"\n    [ERROR] An error occurred: \n {e}")
finally:
    ...
    # Cleaning - For delete repository and Images:
    # ecr.cleanup(repository_name= repository_name)