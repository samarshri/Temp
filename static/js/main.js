/**
 * Student Discussion Forum - Main JavaScript
 * Handles AI features and interactive elements
 */

// Utility function for AJAX requests
async function fetchJSON(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(url, options);
    return await response.json();
}

// Show loading spinner
function showSpinner(button) {
    button.disabled = true;
    button.dataset.originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Loading...';
}

// Hide loading spinner
function hideSpinner(button) {
    button.disabled = false;
    if (button.dataset.originalText) {
        button.innerHTML = button.dataset.originalText;
    }
}

// AI Answer Assistant
document.addEventListener('DOMContentLoaded', function() {
    const askAiBtn = document.getElementById('askAiBtn');
    if (askAiBtn) {
        askAiBtn.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            const responseArea = document.getElementById('aiResponseArea');
            const responseContent = document.getElementById('aiResponseContent');
            
            showSpinner(this);
            
            try {
                const result = await fetchJSON('/ai/answer', 'POST', {post_id: postId});
                
                if (result.success) {
                    responseContent.innerHTML = result.answer.replace(/\n/g, '<br>');
                    responseArea.classList.remove('d-none');
                    
                    // Scroll to response
                    responseArea.scrollIntoView({behavior: 'smooth', block: 'nearest'});
                } else {
                    alert('Failed to get AI response. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            } finally {
                hideSpinner(this);
            }
        });
    }
    
    // AI Thread Summarizer
    const summarizeBtn = document.getElementById('summarizeBtn');
    if (summarizeBtn) {
        summarizeBtn.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            const responseArea = document.getElementById('aiResponseArea');
            const responseContent = document.getElementById('aiResponseContent');
            
            showSpinner(this);
            
            try {
                const result = await fetchJSON('/ai/summarize', 'POST', {post_id: postId});
                
                if (result.success) {
                    responseContent.innerHTML = '<strong>Thread Summary:</strong><br>' + 
                                               result.summary.replace(/\n/g, '<br>');
                    responseArea.classList.remove('d-none');
                    responseArea.scrollIntoView({behavior: 'smooth', block: 'nearest'});
                } else {
                    alert('Failed to generate summary. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            } finally {
                hideSpinner(this);
            }
        });
    }
    
    // AI Content Moderation
    const moderateBtn = document.getElementById('moderateBtn');
    if (moderateBtn) {
        moderateBtn.addEventListener('click', async function() {
            const content = document.getElementById('commentContent').value;
            const resultDiv = document.getElementById('moderationResult');
            
            if (!content.trim()) {
                alert('Please enter a comment first!');
                return;
            }
            
            showSpinner(this);
            
            try {
                const result = await fetchJSON('/ai/moderate', 'POST', {content: content});
                
                resultDiv.className = 'alert mt-3';
                
                if (result.is_safe) {
                    resultDiv.classList.add('alert-success');
                    resultDiv.innerHTML = '<i class="bi bi-check-circle"></i> <strong>Content looks good!</strong> ' + 
                                         result.reason;
                } else {
                    resultDiv.classList.add('alert-warning');
                    resultDiv.innerHTML = '<i class="bi bi-exclamation-triangle"></i> <strong>Warning:</strong> ' + 
                                         result.reason + ' (Confidence: ' + 
                                         (result.confidence * 100).toFixed(0) + '%)';
                }
                
                resultDiv.classList.remove('d-none');
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            } finally {
                hideSpinner(this);
            }
        });
    }
});

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(alert => {
        if (!alert.id || !alert.id.startsWith('ai')) {
            setTimeout(() => {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }, 5000);
        }
    });
});

// Form validation enhancement
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                showSpinner(submitBtn);
            }
        });
    });
});

// Confirm delete actions
document.addEventListener('DOMContentLoaded', function() {
    const deleteForms = document.querySelectorAll('form[action*="/delete"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
});
