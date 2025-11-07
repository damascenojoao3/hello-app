# Projeto CI/CD com Github Actions (app)
Projeto feito no Windows para simular o CI/CD de uma empresa com Github Actions e Argo CD, com o Github como fonte de verdades.  
Argo CD é a ferramenta declarativa de entrega contínua (CD) e de GitOps para o Kubernetes.
# O que foi usado neste repositório
Para este projeto, estes foram os "itens" usados:  
- Github com repositórios públicos  
- Conta no Docker Hub (com token de acesso)  
- Docker desktop  
- Cluster local (Kind) com ArgoCD instalado  
- Git  
- Python 3  
- Kubernetes
Uma recomendação é usar o VS Code com o terminal ativado pra fazer push mais facilmente pro Github, facilita todo o processo.  
Primeiramente, comece com a criação de dois repositórios no Github, um para o os arquivos da aplicação (esse mesmo) e um para os manifestos.  
# App
- 1° Passo  
Dentro da raiz (no Github mesmo ou na pasta no terminal com Git), crie uma pasta chamada ```app```, uma pasta chamada ```.github``` (também na raiz) e, dentro da pasta .github, crie uma pasta chamada ```workflows```. A estrutura deve ficar assim de início:  
hello-app/  
├── .github/  
│   └── workflows/  
└── app/  
- 2° Passo  
Após ter essa estrutura pronta, é hora de adicionar os arquivos:  
em  ```.github/workflows```, adicione o arquivo [ci.yaml](.github/workflows/ci.yaml). Após ter adicionado, volte à pasta app e adicione o arquivo [main.py](app/main.py) e o [arquivo dos requerimentos](app/requirements.txt) (fastapi e uvicorn são os requerimentos listados) e adicione o arquivo [Dockerfile](Dockerfile) na raiz do repositório.  
A estrutura final tem que ficar assim:  
hello-app/  
├── .github/  
│   └── workflows/  
│       └── ci.yaml  
├── app/  
│   ├── main.py  
│   └── requirements.txt  
└── Dockerfile  
Com tudo isso pronto, podemos partir pro próximo passo.  
- 3° Passo  
Ainda aqui, clique em ```Settings```, vá até ```Secrets and variables``` e clique em ```Actions```. Em Actions, é necessária a criação de cinco segredos: ```DOCKER_USERNAME```, ```DOCKER_PASSWORD```, ```SSH_PRIVATE_KEY```, ```MANIFEST_REPO``` e ```GIT_EMAIL```. Eles são usados pelo [ci.yaml](.github/workflows/ci.yaml).  
Os valores guardados em cada segredo têm que ser inseridos manualmente, e para obter os valores:  
**DOCKER_USERNAME**: guarda seu nome (Docker ID) do Docker Hub. É usado para autenticar o Github Actions ao fazer build e push da imagem para o Docker Hub.  
**DOCKER_PASSWORD**: guarda seu Token de Acesso Pessoal (PAT). É a credencial usada com permissão ```Write``` para publicar a imagem no Docker Hub. Para obter uma:  
1. Fazer o login;  
2. Vá no seu ícone e clique em Account Settings;  
3. Navegue até Personal Access Token e clique lá;  
4. Clique em Generate new token;  
5. Dê uma descrição ao token (exemplo: github-actions-app-token);  
6. Mude a permissão para Read & Write;  
7. Clique em Generate;  
8. IMEDIATAMENTE, após o gerar o token, copie o valor completo do token gerado;  
9. Adicione o valor no segredo ```DOCKER_PASSWORD``` (e nunca o compartilhe)  
Assim, é obtido o valor necessário.  
**SSH_PRIVATE_KEY**: é o conteúdo do arquivo ```gitops_key```. Para obté-lo, basta usar este comando:  
```ssh-keygen -t rsa -b 4096 -f gitops_key -C "gitops"```  
e copiar 100% do conteúdo dele para o segredo (ele é usado como uma senha para o Github Actions autenticar e provar que é uma ação sua).  
Ele é usado para gerar um arquivo além do gitops_key, o ```gitops_key.pub```, que é a chave pública.
No meu caso, os arquivos não apareceram no explorador de arquivos padrão, mas apareceram no VS Code, vale a dica.  
**MANIFEST_REPO**: é o URL SSH do repositório dos manifestos, o alvo da operação de GitOps. O link SSH é:  
```git@github.com:seu-user/repositorio-dos-manifestos.git```  
**GIT_EMAIL**: é seu e-mail do Github, basta adicioná-lo ao segredo.  
Com isso, você tem tudo do repositório do app pronto! Mas como o [ci.yaml](.github/workflows/ci.yaml) funciona?
# O arquivo CI
O arquivo [ci.yaml](.github/workflows/ci.yaml) é o principal arquivo da pipeline de Integração Contínua (CI) e implementa a lógica de GitOps ao automatizar a entrega de código. Ele é disparado a cada push na branch main e executa a seguinte sequência de ações:  
1. Build/publicação da imagem  
A Action docker/build-push-action constrói a imagem Docker a partir do Dockerfile e a envia para o Docker Hub. A imagem é "taggeada" com a tag latest e com o SHA do Commit, garantindo a imutabilidade da versão.
2. Update nos manifestos  
Autenticação SSH utiliza o segredo ```SSH_PRIVATE_KEY``` para autenticar de forma segura no repositório hello-manifests e obter permissão de escrita.  
Ao substituir a tag, o workflow clona o hello-manifests, cria uma nova branch e usa um script (comando ```sed```) para substituir a tag antiga da imagem no arquivo deployment.yaml pela nova tag SHA recém-criada, isso cria uma "baixa" junto de uma atualização no pull request.  
Agora que você entendeu o CI, você deve ir ao [repositório dos manifestos](https://github.com/damascenojoao3/hello-manifests)  
Ao fim da etapa deste repositório, ainda não tem nada pronto, mas o mais difícil já foi concluído! No final, sua aplicação estará rodando com essa cara:  
![img](evidencias/app.png)  
