import React, {useEffect, useState} from 'react'

function Header(){
  return (
    <header className="site-header">
      <div className="container">
        <h1>IELTS Prep</h1>
        <p className="subtitle">Практика Listening, Reading, Writing и Speaking</p>
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

export default function App(){
  const [questions, setQuestions] = useState([])

  useEffect(()=>{
    fetch('/api/questions')
      .then(r => r.json())
      .then(setQuestions)
      .catch(()=>setQuestions([]))
  },[])

  return (
    <div>
      <Header />
      <main className="container">
        <section className="grid">
          <Card title="Quick Practice">
            <p>Короткие задания для тренировки навыков IELTS.</p>
            <a className="btn" href="#">Start</a>
          </Card>

          <Card title="Mock Tests">
            <p>Полные тесты в формате экзамена.</p>
            <a className="btn outline" href="#">Try Test</a>
          </Card>

          <Card title="Study Materials">
            <p>Подборки полезных статей и заданий.</p>
            <a className="btn" href="#">Explore</a>
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
      </main>
      <footer className="site-footer">
        <div className="container">© {new Date().getFullYear()} IELTS Prep — сделано для тренировки</div>
      </footer>
    </div>
  )
}
