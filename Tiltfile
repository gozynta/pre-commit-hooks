load("./dev-scripts/Tiltfile", "all_pysrc_py_files")

# If you use any of functions in dev-scripts/Tiltfile then you'll want to pass this
PROJECT_ROOT = '.'
PROJECT_NAME = 'boilerplate'

gar_creds = os.path.join(os.environ.get('HOME'), '.config', 'gcloud', 'application_default_credentials.json')

docker_build(
    'gozynta/' + PROJECT_NAME + '-alpine',
    '.',
    secret='id=gar_creds,src=' + gar_creds,
    dockerfile='Dockerfile.alpine',
    only=['Dockerfile.alpine', 'pyproject.toml','poetry.lock', 'poetry.toml', 'LICENSE'] + all_pysrc_py_files(PROJECT_ROOT)
    )

docker_build(
    'gozynta/' + PROJECT_NAME + '-debian',
    '.',
    secret='id=gar_creds,src=' + gar_creds,
    dockerfile='Dockerfile.debian',
    only=['Dockerfile.debian', 'pyproject.toml','poetry.lock', 'poetry.toml', 'LICENSE'] + all_pysrc_py_files(PROJECT_ROOT)
    )
k8s_yaml('k8s/deployment.yaml')
