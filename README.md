# SI18-CTRL-C
Reposotory para o projeto de SI 2018/2019: Um Gestor de Clipboard Porreirinho

O objetivo principal deste projeto é desenvolver um gestor do Clipboardcom alguma segurança embutida. Estes gestores são programas que permitem guardar todo o histórico da utilização do Clipboard, e até aceder às entradas anteriores com bastante facilidade, sendo esta uma funcionalidade de grande utilidade e uma das principais motivações para a sua existência. O problema é que alguns (senão todos os) gestores de Clipboard guardam o histórico num ficheiro de texto em texto-limpo, inclusive palavras-passe que possam estar a ser copiadas de um gestor de palavras-passe para um formulário online, ficando assim expostas a cavalos de tróia ou até a utilizadores concorrentes do sistema. Pretende-se que o programa desenvolvido no contexto deste projeto resolva esse problema e adicione valor através do suporte das seguintes funcionalidades:
 - [ ] O histórico do Clipboard deve ser guardado cifrado com uma cifra (e modo de cifra) de qualidade reconhecida (e.g., AES);
 - [ ] A chave de cifra deve ser gerada aquando da execução do gestor e guardada apenas em memória. A geração da chave de cifra deve ser feita de forma segura;
 - [ ] O histórico deve ser salvo no disco (cifrado) a cada 5 minutos (apagando o anterior);
 - [ ] Devem ser criados valores de hash de cada entrada no histórico, que devem ser guardados em texto limpo num ficheiro à parte;
 - [ ] Deve ser possível verificar se determinada entrada existe no último ficheiro do histórico cifrado, sem o decifrar, e recorrendo apenas aos valores de hash;
 - [ ] Deve ser feita uma assinatura digital do ficheiro cifrado aquando este é guardado no disco (i.e., a cada 5 minutos). Para tal, deve ser gerado um par de chaves RSA que acompanha a aplicação.
 
 
 Este projeto pressupõe o desenvolvimento de uma aplicação que procura obter as entradas
do Clipboard em segundo plano. Para tal, pode pensar em colocá-la a correr como um daemon que faz CTRL+V a cada 2 segundos, na expetativa de encontrar uma entrada nova. Eventualmente, pode ainda desenvolver uma aplicação para configuração de alguns parâmetros (e.g., quantas entradas são suportadas). A aplicação principal deve permitir ver as várias entradas no Clipboard e também escolher qual deve ir para lá através de duplo clique. Note que a versão mais simples da aplicação, o histórico é perdido sempre que esta é terminada (porque a chave de cifra que permite decifrar o ficheiro está apenas guardada em memória).

Uma versão mais elaborada da aplicação deve ter funcionalidades adicionais, como as
que se sugerem a seguir:
 - [ ] O gestor deve suportar a geração de chaves de cifra a partir de uma pitada de sal e de uma palavra-passe mestra, configurada pelo utilizador aquando da primeira utilização. Deve ser usada, para o efeito, uma função de derivação de chaves de cifra como a PBKDF2;
 - [ ] Tomando a funcionalidade anterior como garantida, o gestor deve conseguir decifrar ficheiros de históricos anteriores;
 - [ ] Tomando a funcionalidade anterior como garantida, o gestor deve conseguir decifrar, de forma muito seletiva, apenas as entradas selecionadas pelo utilizador. Esta funcionalidade requer que seja usado um modo de cifra adequado;
 - [ ] O gestor deve suportar vários utilizadores (cada utilizador terá o seu histórico);
 - [ ] As assinaturas devem ser verificadas a pedido do utilizador;
 - [ ] Permitir que os programas cliente utilizem certificados digitais para validação das assinaturas digitais;
 - [ ] Escrever um help bastante completo.
 
- [ ] Pensem numa forma de atacar o sistema (uma falha da sua implementação) e dediquem-
lhe uma secção no relatório. 
