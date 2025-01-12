import React, { useState, useRef, useEffect } from 'react';
import { Send, Moon, Sun, Menu, Plus, Search, MoreVertical, Settings, Copy, RefreshCw, ChevronLeft, ChevronRight, Image, FileText, Camera, Sparkles, X, ChevronDown } from 'lucide-react';

type Mensagem = {
  texto: string;
  isBot: boolean;
};

type Conversa = {
  id: string;
  titulo: string;
  mensagens: Mensagem[];
  modelo: string;
};

type ModeloGPT = {
  id: string;
  nome: string;
  descricao: string;
};

function App() {
  const [conversas, setConversas] = useState<Conversa[]>([]);
  const [conversaAtual, setConversaAtual] = useState<string | null>(null);
  const [inputTexto, setInputTexto] = useState("");
  const [temaEscuro, setTemaEscuro] = useState(false);
  const [menuAberto, setMenuAberto] = useState(false);
  const [barraLateralVisivel, setBarraLateralVisivel] = useState(true);
  const [termoBusca, setTermoBusca] = useState("");
  const [modeloSelecionado, setModeloSelecionado] = useState("gpt-4");
  const [menuModeloAberto, setMenuModeloAberto] = useState(false);
  const chatRef = useRef<HTMLDivElement>(null);

  const modelos: ModeloGPT[] = [
    { id: 'gpt-4', nome: 'GPT-4', descricao: 'Mais capaz e atualizado' },
    { id: 'gpt-3.5', nome: 'GPT-3.5', descricao: 'Mais rápido e econômico' },
    { id: 'gpt-4-vision', nome: 'GPT-4 Vision', descricao: 'Análise de imagens' },
  ];

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [conversas]);

  useEffect(() => {
    if (temaEscuro) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [temaEscuro]);

  const enviarMensagem = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputTexto.trim()) return;

    let idConversa = conversaAtual;
    if (!idConversa) {
      idConversa = String(Date.now());
      const novaConversa: Conversa = {
        id: idConversa,
        titulo: inputTexto.slice(0, 30) + (inputTexto.length > 30 ? '...' : ''),
        mensagens: [],
        modelo: modeloSelecionado
      };
      setConversas(prev => [...prev, novaConversa]);
      setConversaAtual(idConversa);
    }

    const novaMensagem = { texto: inputTexto, isBot: false };
    
    setConversas(prevConversas => {
      return prevConversas.map(conv => {
        if (conv.id === idConversa) {
          return {
            ...conv,
            mensagens: [...conv.mensagens, novaMensagem]
          };
        }
        return conv;
      });
    });

    setTimeout(() => {
      const respostaBot = {
        texto: `[${modeloSelecionado}] Desculpe, sou apenas uma demonstração. Não posso realmente processar sua mensagem.`,
        isBot: true
      };
      setConversas(prevConversas => {
        return prevConversas.map(conv => {
          if (conv.id === idConversa) {
            return {
              ...conv,
              mensagens: [...conv.mensagens, respostaBot]
            };
          }
          return conv;
        });
      });
    }, 1000);

    setInputTexto("");
  };

  const novaConversa = () => {
    setConversaAtual(null);
    setInputTexto("");
  };

  const copiarMensagem = (texto: string) => {
    navigator.clipboard.writeText(texto);
  };

  const regenerarResposta = (index: number) => {
    const respostaBot = {
      texto: `[${modeloSelecionado}] Esta é uma nova resposta regenerada (simulação).`,
      isBot: true
    };
    
    setConversas(prevConversas => {
      return prevConversas.map(conv => {
        if (conv.id === conversaAtual) {
          const novasMensagens = [...conv.mensagens];
          novasMensagens[index] = respostaBot;
          return {
            ...conv,
            mensagens: novasMensagens
          };
        }
        return conv;
      });
    });
  };

  const conversaAtualObj = conversas.find(c => c.id === conversaAtual);
  const mensagensAtuais = conversaAtualObj?.mensagens || [];

  const conversasFiltradas = conversas.filter(conv => 
    conv.titulo.toLowerCase().includes(termoBusca.toLowerCase())
  );

  const funcaoSimulada = (funcao: string) => {
    const novaId = String(Date.now());
    const novaConversa: Conversa = {
      id: novaId,
      titulo: funcao,
      mensagens: [{ texto: `[${modeloSelecionado}] Iniciando ${funcao.toLowerCase()}...`, isBot: true }],
      modelo: modeloSelecionado
    };
    setConversas(prev => [...prev, novaConversa]);
    setConversaAtual(novaId);
  };

  return (
    <div className={`min-h-screen flex ${temaEscuro ? 'dark' : ''}`}>
      {/* Overlay para fechar a barra lateral em telas pequenas */}
      {barraLateralVisivel && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 md:hidden"
          onClick={() => setBarraLateralVisivel(false)}
        />
      )}

      {/* Barra Lateral */}
      <div 
        className={`fixed inset-y-0 left-0 z-30 w-72 transform transition-transform duration-300 ease-in-out 
          ${barraLateralVisivel ? 'translate-x-0' : '-translate-x-full'}
          bg-white dark:bg-dark-primary border-r border-gray-200 dark:border-dark-border
          md:relative md:translate-x-0`}
      >
        {/* Botão de fechar em telas pequenas */}
        <button
          onClick={() => setBarraLateralVisivel(false)}
          className="absolute top-4 right-4 p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-secondary md:hidden"
        >
          <X className="h-5 w-5 text-gray-500 dark:text-dark-text-secondary" />
        </button>

        <div className="flex flex-col h-full">
          <div className="p-4">
            <button
              onClick={novaConversa}
              className="w-full flex items-center justify-center gap-2 p-2 rounded-lg
                border border-gray-300 dark:border-dark-border
                hover:bg-gray-100 dark:hover:bg-dark-secondary
                text-gray-700 dark:text-dark-text-primary
                transition-colors"
            >
              <Plus className="h-5 w-5" />
              Nova Conversa
            </button>

            {/* Seletor de Modelo */}
            <div className="relative mt-4">
              <button
                onClick={() => setMenuModeloAberto(!menuModeloAberto)}
                className="w-full flex items-center justify-between p-2 rounded-lg
                  border border-gray-300 dark:border-dark-border
                  hover:bg-gray-100 dark:hover:bg-dark-secondary
                  text-gray-700 dark:text-dark-text-primary
                  transition-colors"
              >
                <div className="flex items-center gap-2">
                  <span>{modelos.find(m => m.id === modeloSelecionado)?.nome || modeloSelecionado}</span>
                </div>
                <ChevronDown className="h-4 w-4" />
              </button>

              {menuModeloAberto && (
                <div className="absolute w-full mt-2 bg-white dark:bg-dark-secondary rounded-lg shadow-lg border border-gray-200 dark:border-dark-border z-50">
                  {modelos.map(modelo => (
                    <button
                      key={modelo.id}
                      onClick={() => {
                        setModeloSelecionado(modelo.id);
                        setMenuModeloAberto(false);
                      }}
                      className="w-full text-left p-3 hover:bg-gray-100 dark:hover:bg-dark-border first:rounded-t-lg last:rounded-b-lg"
                    >
                      <div className="font-medium text-gray-800 dark:text-dark-text-primary">
                        {modelo.nome}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-dark-text-secondary">
                        {modelo.descricao}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Busca */}
          <div className="px-4 mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 dark:text-dark-text-secondary" />
              <input
                type="text"
                placeholder="Buscar conversas..."
                value={termoBusca}
                onChange={(e) => setTermoBusca(e.target.value)}
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-dark-border
                  bg-white dark:bg-dark-secondary text-gray-800 dark:text-dark-text-primary
                  focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Lista de Conversas */}
          <div className="flex-1 overflow-y-auto">
            {conversasFiltradas.map((conv) => (
              <div
                key={conv.id}
                className={`flex items-center justify-between p-3 cursor-pointer
                  hover:bg-gray-100 dark:hover:bg-dark-secondary
                  ${conv.id === conversaAtual ? 'bg-gray-200 dark:bg-dark-secondary' : ''}`}
                onClick={() => setConversaAtual(conv.id)}
              >
                <span className="truncate text-gray-800 dark:text-dark-text-primary">{conv.titulo}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                  }}
                  className="p-1 hover:bg-gray-200 dark:hover:bg-dark-border rounded-full"
                >
                  <MoreVertical className="h-4 w-4 text-gray-500 dark:text-dark-text-secondary" />
                </button>
              </div>
            ))}
          </div>

          {/* Rodapé da Barra Lateral */}
          <div className="p-4 border-t dark:border-dark-border">
            <button
              onClick={() => setTemaEscuro(!temaEscuro)}
              className="flex items-center gap-2 p-2 w-full rounded-lg
                hover:bg-gray-100 dark:hover:bg-dark-secondary
                text-gray-700 dark:text-dark-text-primary"
            >
              {temaEscuro ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
              {temaEscuro ? 'Modo Claro' : 'Modo Escuro'}
            </button>
            <button
              className="flex items-center gap-2 p-2 w-full rounded-lg
                hover:bg-gray-100 dark:hover:bg-dark-secondary
                text-gray-700 dark:text-dark-text-primary mt-2"
            >
              <Settings className="h-5 w-5" />
              Configurações
            </button>
          </div>
        </div>
      </div>

      {/* Botão Toggle Barra Lateral */}
      <button
        onClick={() => setBarraLateralVisivel(!barraLateralVisivel)}
        className={`fixed z-40 p-3 rounded-lg transition-all duration-300 ease-in-out
          ${barraLateralVisivel 
            ? 'left-72 bg-transparent' 
            : 'left-4 bg-white dark:bg-dark-secondary shadow-lg'}
          bottom-4 md:hidden`}
      >
        {barraLateralVisivel ? (
          <ChevronLeft className="h-6 w-6 text-gray-600 dark:text-dark-text-secondary" />
        ) : (
          <Menu className="h-6 w-6 text-gray-600 dark:text-dark-text-secondary" />
        )}
      </button>

      {/* Conteúdo Principal */}
      <div className="flex-1 flex flex-col min-h-screen bg-gray-50 dark:bg-dark-primary">
        {/* Navbar */}
        <nav className="bg-white dark:bg-dark-secondary shadow-md">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <button
                  onClick={() => setMenuAberto(!menuAberto)}
                  className="md:hidden p-2"
                >
                  <Menu className="h-6 w-6 text-gray-700 dark:text-dark-text-secondary" />
                </button>
                <span className="text-xl font-bold text-gray-800 dark:text-dark-text-primary ml-2">
                  ChatGPT Clone
                </span>
              </div>
            </div>
          </div>
        </nav>

        {/* Conteúdo do Chat ou Tela Inicial */}
        {conversaAtual ? (
          // Área do Chat
          <div ref={chatRef} className="flex-1 p-4 space-y-4 overflow-y-auto">
            {mensagensAtuais.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.isBot ? 'justify-start' : 'justify-end'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    msg.isBot
                      ? 'bg-white dark:bg-dark-secondary text-gray-800 dark:text-dark-text-primary'
                      : 'bg-dark-accent text-white'
                  }`}
                >
                  <div className="flex flex-col gap-2">
                    <p>{msg.texto}</p>
                    {msg.isBot && (
                      <div className="flex gap-2 mt-2">
                        <button
                          onClick={() => copiarMensagem(msg.texto)}
                          className="p-1 hover:bg-gray-100 dark:hover:bg-dark-border rounded"
                          title="Copiar mensagem"
                        >
                          <Copy className="h-4 w-4 text-gray-500 dark:text-dark-text-secondary" />
                        </button>
                        <button
                          onClick={() => regenerarResposta(index)}
                          className="p-1 hover:bg-gray-100 dark:hover:bg-dark-border rounded"
                          title="Regenerar resposta"
                        >
                          <RefreshCw className="h-4 w-4 text-gray-500 dark:text-dark-text-secondary" />
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          // Tela Inicial
          <div className="flex-1 flex flex-col items-center justify-center p-4">
            <h1 className="text-4xl font-bold mb-8 text-gray-800 dark:text-dark-text-primary">
              Como posso ajudar?
            </h1>
            
            <div className="w-full max-w-2xl mb-8">
              <form onSubmit={enviarMensagem} className="w-full">
                <input
                  type="text"
                  value={inputTexto}
                  onChange={(e) => setInputTexto(e.target.value)}
                  placeholder="Envie uma mensagem para o ChatGPT"
                  className="w-full p-4 text-lg border rounded-lg
                    bg-white dark:bg-dark-secondary
                    text-gray-800 dark:text-dark-text-primary
                    border-gray-300 dark:border-dark-border
                    focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </form>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <button
                onClick={() => funcaoSimulada("Criar imagem")}
                className="flex items-center gap-2 p-4 bg-white dark:bg-dark-secondary rounded-lg
                  shadow-md hover:shadow-lg transition-shadow
                  text-gray-800 dark:text-dark-text-primary"
              >
                <Image className="h-5 w-5" />
                <span>Criar imagem</span>
              </button>
              <button
                onClick={() => funcaoSimulada("Sugerir")}
                className="flex items-center gap-2 p-4 bg-white dark:bg-dark-secondary rounded-lg
                  shadow-md hover:shadow-lg transition-shadow
                  text-gray-800 dark:text-dark-text-primary"
              >
                <Sparkles className="h-5 w-5" />
                <span>Sugerir</span>
              </button>
              <button
                onClick={() => funcaoSimulada("Resumir texto")}
                className="flex items-center gap-2 p-4 bg-white dark:bg-dark-secondary rounded-lg
                  shadow-md hover:shadow-lg transition-shadow
                  text-gray-800 dark:text-dark-text-primary"
              >
                <FileText className="h-5 w-5" />
                <span>Resumir texto</span>
              </button>
              <button
                onClick={() => funcaoSimulada("Analisar imagens")}
                className="flex items-center gap-2 p-4 bg-white dark:bg-dark-secondary rounded-lg
                  shadow-md hover:shadow-lg transition-shadow
                  text-gray-800 dark:text-dark-text-primary"
              >
                <Camera className="h-5 w-5" />
                <span>Analisar imagens</span>
              </button>
            </div>
          </div>
        )}

        {/* Barra de Input (apenas visível quando uma conversa está ativa) */}
        {conversaAtual && (
          <div className="p-4 bg-white dark:bg-dark-secondary border-t dark:border-dark-border">
            <form onSubmit={enviarMensagem} className="max-w-3xl mx-auto">
              <div className="flex items-center space-x-2">
                <input
                  type="text"
                  value={inputTexto}
                  onChange={(e) => setInputTexto(e.target.value)}
                  placeholder="Digite sua mensagem..."
                  className="flex-1 p-2 border rounded-lg
                    bg-white dark:bg-dark-secondary
                    text-gray-800 dark:text-dark-text-primary
                    border-gray-300 dark:border-dark-border
                    focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="submit"
                  className="p-2 bg-dark-accent text-white rounded-lg
                    hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-dark-accent"
                >
                  <Send className="h-5 w-5" />
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;