import React, {useEffect, useState} from 'react'

function Header({onNavigate}){
  return (
    <header className="site-header">
      <div className="container" style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          <h1>IELTS Prep</h1>
          <p className="subtitle">Практика Listening, Reading, Writing и Speaking</p>
        </div>
        <nav>
          <button className="btn outline" onClick={() => onNavigate('home')}>Home</button>
          <button className="btn outline" onClick={() => onNavigate('practice')} style={{marginLeft:8}}>Practice</button>
          <button className="btn outline" onClick={() => onNavigate('tests')} style={{marginLeft:8}}>Tests</button>
          <button className="btn outline" onClick={() => onNavigate('materials')} style={{marginLeft:8}}>Materials</button>
        </nav>
      </div>
    </header>
  )
}

function Card({title, children}){
  return (
    <div className="card">
      <h3>{title}</h3>
      <div className="card-body">{children}</div>
    </div>
  )
}

function TestView({onBack}){
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(()=>{
    fetch('/api/questions')
      .then(r => r.json())
      .then(setQuestions)
      .catch(()=>setQuestions([]))
  },[])

  function setAnswer(id, value){
    setAnswers(prev => ({...prev, [id]: value}))
  }

  async function submit(){
    setLoading(true)
    try{
      const res = await fetch('/api/score', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({answers})
      })
      const json = await res.json()
      setResult(json)
    }catch(e){
      setResult({error: String(e)})
    }finally{setLoading(false)}
  }

  return (
    <div>
      <div style={{marginBottom:12}}>
        <button className="btn outline" onClick={onBack}>← Back</button>
      </div>
      <h2>Тест</h2>
      {questions.length===0 && <p>Нет доступных вопросов.</p>}
      {questions.map(q=> (
        <div className="question" key={q.id} style={{marginBottom:12}}>
          <div className="q-meta">{q.part} • #{q.id}</div>
          <div className="q-prompt">{q.prompt}</div>
          {q.choices && q.choices.length>0 ? (
            <div className="choices" style={{marginTop:8}}>
              {q.choices.map((c,i)=> (
                <label key={i} style={{display:'block',marginBottom:6}}>
                  <input type="radio" name={`q_${q.id}`} value={c} checked={answers[q.id]===c} onChange={(e)=>setAnswer(q.id, e.target.value)} /> {c}
                </label>
              ))}
            </div>
          ) : (
            <textarea placeholder="Ваш ответ" value={answers[q.id]||''} onChange={(e)=>setAnswer(q.id, e.target.value)} style={{width:'100%',minHeight:80,marginTop:8}} />
          )}
        </div>
      ))}

      <div style={{marginTop:12}}>
        <button className="btn" onClick={submit} disabled={loading}>{loading ? 'Submitting...' : 'Submit answers'}</button>
      </div>

      {result && (
        <div className="card" style={{marginTop:16}}>
          <h3>Result</h3>
          <div className="card-body">
            {result.error && <div style={{color:'salmon'}}>{result.error}</div>}
            {result.message && <div>{result.message}</div>}
            {result.score!==undefined && (
              <div>Score: {result.score} / {result.total} ({result.percent}%)</div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default function App(){
  const [view, setView] = useState('home')
  const [questions, setQuestions] = useState([])

  useEffect(()=>{
    fetch('/api/questions')
      .then(r => r.json())
      .then(setQuestions)
      .catch(()=>setQuestions([]))
  },[])

  return (
    <div>
      <Header onNavigate={setView} />
      <main className="container">
        {view === 'home' && (
          <>
            <section className="grid">
              <Card title="Quick Practice">
                <p>Короткие задания для тренировки навыков IELTS.</p>
                <button className="btn" onClick={() => setView('practice')}>Start</button>
              </Card>

              <Card title="Mock Tests">
                <p>Полные тесты в формате экзамена.</p>
                <button className="btn outline" onClick={() => setView('tests')}>Try Test</button>
              </Card>

              <Card title="Study Materials">
                <p>Подборки полезных статей и заданий.</p>
                <button className="btn" onClick={() => setView('materials')}>Explore</button>
              </Card>
            </section>

            <section>
              <h2>Примеры вопросов</h2>
              <div className="questions">
                {questions.length === 0 && <p>Нет данных (запрос к `/api/questions` не удался).</p>}
                {questions.map(q => (
                  <div className="question" key={q.id}>
                    <div className="q-meta">{q.part} • #{q.id}</div>
                    <div className="q-prompt">{q.prompt}</div>
                    {q.choices && q.choices.length>0 && (
                      <ul className="choices">{q.choices.map((c,i)=>(<li key={i}>{c}</li>))}</ul>
                    )}
                  </div>
                ))}
              </div>
            </section>
          </>
        )}

        {view === 'practice' && (
          <div>
            <button className="btn outline" onClick={() => setView('home')}>← Back</button>
            <h2>Quick Practice</h2>
            <p>Здесь будут короткие задания. Для примера откройте полный тест:</p>
            <button className="btn" onClick={() => setView('tests')}>Open Mock Test</button>
          </div>
        )}

        {view === 'tests' && (
          <TestView onBack={() => setView('home')} />
        )}

        {view === 'materials' && (
          <div>
            <button className="btn outline" onClick={() => setView('home')}>← Back</button>
            <h2>Study Materials</h2>
            <p>Здесь будут статьи и материалы для подготовки.</p>
          </div>
        )}
      </main>
      <footer className="site-footer">
        <div className="container">© {new Date().getFullYear()} IELTS Prep — сделано для тренировки</div>
      </footer>
    </div>
  )
}
