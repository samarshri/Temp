import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
    return (
        <footer className="bg-white border-top py-5 mt-auto">
            <div className="container">
                <div className="row g-4">
                    <div className="col-lg-4">
                        <div className="d-flex align-items-center gap-2 mb-3">
                            <div className="d-flex align-items-center justify-content-center bg-primary text-white rounded-circle" style={{ width: '32px', height: '32px' }}>
                                <i className="bi bi-mortarboard-fill small"></i>
                            </div>
                            <span className="fw-bold text-primary">Student Discussion Forum</span>
                        </div>
                        <p className="small text-muted mb-3">
                            A Web-based Platform for Academic Collaboration. Designed to foster learning, peer support, and knowledge sharing within the campus community.
                        </p>
                        <div className="d-flex gap-3">
                            <a href="#" className="text-muted"><i className="bi bi-github"></i></a>
                            <a href="#" className="text-muted"><i className="bi bi-linkedin"></i></a>
                            <a href="#" className="text-muted"><i className="bi bi-globe"></i></a>
                        </div>
                    </div>

                    <div className="col-lg-2 col-6">
                        <h6 className="fw-bold mb-3 small text-uppercase">Project</h6>
                        <ul className="list-unstyled small text-muted d-flex flex-column gap-2 mb-0">
                            <li>About Us</li>
                            <li>Major Project</li>
                            <li>Documentation</li>
                            <li>Report Issue</li>
                        </ul>
                    </div>

                    <div className="col-lg-2 col-6">
                        <h6 className="fw-bold mb-3 small text-uppercase">Legal</h6>
                        <ul className="list-unstyled small text-muted d-flex flex-column gap-2 mb-0">
                            <li>Privacy Policy</li>
                            <li>Terms of Service</li>
                            <li>Academic Integrity</li>
                            <li>Guidelines</li>
                        </ul>
                    </div>

                    <div className="col-lg-4">
                        <div className="p-3 bg-light rounded-3 border">
                            <h6 className="fw-bold mb-2 small text-uppercase">Project Details</h6>
                            <ul className="list-unstyled small text-muted mb-0">
                                <li className="mb-1"><span className="fw-bold">College:</span> [Your College Name]</li>
                                <li className="mb-1"><span className="fw-bold">Department:</span> Computer Science & Engineering</li>
                                <li className="mb-1"><span className="fw-bold">Batch:</span> 2022-2026</li>
                                <li className="mb-1 pt-2 border-top mt-2"><span className="fw-bold">Team Members:</span></li>
                                <li>Member 1, Member 2, Member 3</li>
                                <li className="pt-2"><span className="fw-bold">Project Guide:</span> Prof. [Guide Name]</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div className="text-center pt-4 mt-4 border-top">
                    <p className="small text-muted mb-0">
                        &copy; {new Date().getFullYear()} Student Discussion Forum. Major Project Declaration.
                    </p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
