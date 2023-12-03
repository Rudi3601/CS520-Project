//Routes.js
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App.js";
import NotFound from './components/NotFound.js';
import DoctorLogin from './components/DoctorLogin.js';
import DoctorPortal from './components/DoctorPortal.js';

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" exact component={App} element={<App/>} />
        <Route exact component={NotFound} />
        <Route path="/DoctorLogin" exact component={DoctorLogin} element={<DoctorLogin/>} />
        <Route path="/DoctorPortal" exact component={DoctorPortal} element={<DoctorPortal/>} />
      </Routes>
    </BrowserRouter>
  );
};

export default Router;