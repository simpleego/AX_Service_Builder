import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'
import Layout from './component/Layout'
import Header from './component/Header'
import Footer from './component/Footer'
import CommentList from './chapter_05/CommentList'
import NotificationList from './chapter_06/NotificationList'
import Counter from './chapter_06/Counter'
import UserProfile from './chapter_06/UserProfile'
import Clock from './chapter_06/Clock'
import WindowSize from './chapter_06/WindowSize'
import NotificationTitle from './chapter_06/NotificationTitle'
import TodoInput from './chapter_06/TodoInput'
import ChatRoom from './chapter_06/ChatRoom'

function App() {

  return (
    <>
     <ChatRoom roomId={1}/>
     <ChatRoom roomId={2}/>
     <ChatRoom roomId={3}/>
    </>
  )
}

export default App
