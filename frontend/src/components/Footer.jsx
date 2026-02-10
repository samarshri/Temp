import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
    return (
        <footer className="bg-white py-5 mt-auto">
            <div className="container text-center">
                <div className="text-muted small">
                    <p className="fw-bold mb-1">Student Discussion Forum</p>
                    <p className="mb-4">A Web-based Platform for Academic Collaboration</p>

                    <div className="mb-4">
                        <p className="mb-1">Major Project – [Your College Name]</p>
                        <p className="mb-1">Department of Computer Science & Engineering</p>
                        <p className="mb-0">Batch: 2022–2026</p>
                    </div>

                    <div className="mb-4">
                        <p className="fw-bold mb-1">Developed by:</p>
                        <ul className="list-unstyled mb-0">
                            <li>Nitin Pathekar</li>
                            <li>Samar Shrivastava</li>
                            <li>Gaurav Parihar</li>
                            <li>Sambhav Jain</li>
                        </ul>
                    </div>

                    <p className="mb-0">Project Guide: Prof. [Guide Name]</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
