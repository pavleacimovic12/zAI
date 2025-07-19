// Chat functionality for the Q-Learning AI Agent

let chatHistory = [];
let isProcessing = false;
let selectedFile = null;
let pinnedFiles = [];

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize file upload functionality
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    
    if (uploadBtn && fileInput) {
        uploadBtn.addEventListener('click', function() {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                selectedFile = file;
                fileName.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
                filePreview.style.display = 'block';
                
                // Add pin option to file preview
                if (!document.getElementById('pinBtn')) {
                    const pinBtn = document.createElement('button');
                    pinBtn.id = 'pinBtn';
                    pinBtn.className = 'btn btn-outline-primary btn-sm ms-2';
                    pinBtn.innerHTML = '<i class="fas fa-thumbtack"></i> Pin';
                    pinBtn.title = 'Pin this file for easy re-upload';
                    pinBtn.onclick = function() {
                        pinFile(selectedFile);
                    };
                    document.getElementById('filePreview').querySelector('.alert').appendChild(pinBtn);
                }
            }
        });
    }
    
    // Initialize MRI file upload functionality
    const mriFileInput = document.getElementById('mriFileInput');
    if (mriFileInput) {
        mriFileInput.addEventListener('change', function(event) {
            const files = event.target.files;
            if (files.length > 0) {
                // Auto-analyze MRI files when selected
                analyzeMRIFiles(files);
            }
        });
    }
    
    // Initialize drag and drop functionality
    const dragDropZone = document.getElementById('dragDropZone');
    if (dragDropZone) {
        // Click to select files
        dragDropZone.addEventListener('click', function() {
            document.getElementById('fileInput').click();
        });
        
        // Drag and drop events
        dragDropZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dragDropZone.classList.add('drag-over');
        });
        
        dragDropZone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dragDropZone.classList.remove('drag-over');
        });
        
        dragDropZone.addEventListener('drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dragDropZone.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleDroppedFiles(files);
            }
        });
    }
});

function clearFileSelection() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('filePreview').style.display = 'none';
    
    // Remove pin button if it exists
    const pinBtn = document.getElementById('pinBtn');
    if (pinBtn) {
        pinBtn.remove();
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Handle enter key press in chat input
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Send message to the agent
async function sendMessage() {
    console.log('sendMessage function called');
    const input = document.getElementById('user-input');
    console.log('Input element:', input);
    if (!input) {
        console.error('Could not find user-input element');
        return;
    }
    const query = input.value.trim();
    console.log('Query:', query);
    
    // Check if we have a file selected but no text query
    if (!query && !selectedFile) return;
    if (isProcessing) return;
    
    isProcessing = true;
    input.value = '';
    input.disabled = true;
    
    // Store file reference before clearing
    const fileToUpload = selectedFile;
    
    // Add user message to chat
    let userMessage = query;
    if (fileToUpload) {
        userMessage = query || `Uploaded file: ${fileToUpload.name}`;
        userMessage += ` 📎 ${fileToUpload.name}`;
    }
    addMessage(userMessage, 'user');
    
    // Clear file selection after creating message
    if (fileToUpload) {
        clearFileSelection();
    }
    
    // Create a placeholder for the streaming response
    const responseElement = addStreamingMessage();
    
    try {
        let response;
        
        if (fileToUpload) {
            // Handle file upload
            const formData = new FormData();
            formData.append('file', fileToUpload);
            
            response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
        } else {
            // Handle regular chat message
            console.log('Sending chat request:', { query: query, preview: window.location.pathname.includes('preview') });
            
            response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    query: query, 
                    preview: window.location.pathname.includes('preview') 
                })
            });
        }
        
        if (!response.ok) {
            const errorData = await response.json();
            removeStreamingMessage(responseElement);
            addMessage(errorData.error || 'Sorry, I encountered an error processing your request.', 'agent');
            return;
        }
        
        if (fileToUpload) {
            // Handle file upload response
            const data = await response.json();
            removeStreamingMessage(responseElement);
            
            if (data.result) {
                const result = data.result;
                let analysisMessage = '';
                
                if (result.type === 'image') {
                    analysisMessage = `**Image Analysis: ${result.filename}**\n\n${result.analysis}`;
                } else if (result.type === 'pdf') {
                    analysisMessage = `**PDF Analysis: ${result.filename}**\n\n${result.summary}`;
                } else if (result.type === 'text') {
                    analysisMessage = `**Document Analysis: ${result.filename}**\n\n${result.analysis}`;
                } else if (result.type === 'mri') {
                    analysisMessage = `**MRI Analysis: ${result.filename}**\n\n${result.analysis}`;
                    
                    // Add brain slice images if available
                    if (result.slice_images && result.slice_images.slices) {
                        analysisMessage += '\n\n**Brain Slice Images:**\n';
                        const slices = result.slice_images.slices;
                        
                        if (slices.axial) {
                            analysisMessage += `\n<img src="${slices.axial}" alt="Axial Slice" style="max-width: 300px; margin: 10px;" title="Axial (Top-Bottom) View">`;
                        }
                        if (slices.coronal) {
                            analysisMessage += `\n<img src="${slices.coronal}" alt="Coronal Slice" style="max-width: 300px; margin: 10px;" title="Coronal (Front-Back) View">`;
                        }
                        if (slices.sagittal) {
                            analysisMessage += `\n<img src="${slices.sagittal}" alt="Sagittal Slice" style="max-width: 300px; margin: 10px;" title="Sagittal (Left-Right) View">`;
                        }
                        
                        analysisMessage += '\n\n*Brain slices shown from different anatomical planes for comprehensive visualization.*';
                    }
                } else if (result.error) {
                    analysisMessage = `**Error analyzing ${result.filename}**: ${result.error}`;
                }
                
                // Format the message with proper spacing
                analysisMessage = analysisMessage.replace(/\n\n/g, '\n\n');
                analysisMessage = analysisMessage.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                analysisMessage = analysisMessage.replace(/\n/g, '<br>');
                analysisMessage = analysisMessage.replace(/<br><br>/g, '<br><br>');
                
                addMessage(analysisMessage, 'agent');
            } else {
                addMessage('File uploaded successfully but no analysis available.', 'agent');
            }
        } else {
            // Handle streaming chat response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop(); // Keep incomplete line in buffer
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.substring(6));
                            if (data.chunk) {
                                appendToStreamingMessage(responseElement, data.chunk);
                            } else if (data.chart) {
                                // Add chart visualization to response
                                addChartToMessage(responseElement, data.chart);
                            } else if (data.done) {
                                finalizeStreamingMessage(responseElement);
                                chatHistory.push({ query, response: responseElement.textContent });
                            } else if (data.error) {
                                removeStreamingMessage(responseElement);
                                addMessage(`Error: ${data.error}`, 'agent');
                            }
                        } catch (e) {
                            console.error('Error parsing SSE data:', e);
                            console.error('Error details:', e.message, line);
                            // If we can't parse as JSON, treat as plain text response
                            if (line.startsWith('data: ') && line.length > 6) {
                                const text = line.substring(6);
                                if (text.trim()) {
                                    appendToStreamingMessage(responseElement, text + ' ');
                                }
                            }
                        }
                    }
                }
            }
        }
        
    } catch (error) {
        console.error('Chat error:', error);
        console.error('Error details:', error.message, error.stack);
        removeStreamingMessage(responseElement);
        
        // More specific error messages
        let errorMessage = 'Sorry, I\'m having trouble connecting right now. Please try again.';
        
        if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Network connection issue. Please check your internet connection and try again.';
        } else if (error.message.includes('NetworkError')) {
            errorMessage = 'Network error occurred. Please refresh the page and try again.';
        } else if (error.name === 'AbortError') {
            errorMessage = 'Request was cancelled. Please try again.';
        }
        
        addMessage(errorMessage, 'agent');
    } finally {
        isProcessing = false;
        input.disabled = false;
        input.focus();
    }
}

// Add chart to streaming message
function addChartToMessage(messageElement, chartHtml) {
    const chartContainer = document.createElement('div');
    chartContainer.className = 'chart-container mt-3';
    chartContainer.innerHTML = chartHtml;
    messageElement.appendChild(chartContainer);
    
    // Scroll to bottom to show the chart
    const chatContainer = document.getElementById('chat-messages');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Add message to chat container
function addMessage(content, sender) {
    console.log('Adding message:', content, 'from:', sender);
    const chatContainer = document.getElementById('chat-messages');
    console.log('Chat container:', chatContainer);
    if (!chatContainer) {
        console.error('Could not find chat-messages container');
        return;
    }
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const messageContentDiv = document.createElement('div');
    messageContentDiv.className = sender === 'user' ? 'user-message' : 'agent-message';
    
    // Format content with proper spacing and markdown
    let formattedContent = content;
    formattedContent = formattedContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedContent = formattedContent.replace(/\n\n/g, '<br><br>');
    formattedContent = formattedContent.replace(/\n/g, '<br>');
    messageContentDiv.innerHTML = `<div class="message-text">${formattedContent}</div>`;
    
    messageDiv.appendChild(messageContentDiv);
    chatContainer.appendChild(messageDiv);
    
    // Process any embedded chart containers
    processEmbeddedCharts(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Add streaming message placeholder
function addStreamingMessage() {
    const chatContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent streaming';
    
    const messageContentDiv = document.createElement('div');
    messageContentDiv.className = 'agent-message';
    messageContentDiv.innerHTML = '<div class="message-text"></div>';
    
    messageDiv.appendChild(messageContentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return messageDiv;
}

// Append content to streaming message
function appendToStreamingMessage(messageElement, content) {
    const textDiv = messageElement.querySelector('.message-text');
    textDiv.textContent += content;
    
    // Apply real-time formatting for better readability
    let formattedContent = textDiv.textContent;
    formattedContent = formattedContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedContent = formattedContent.replace(/\n\n/g, '<br><br>');
    formattedContent = formattedContent.replace(/\n/g, '<br>');
    textDiv.innerHTML = formattedContent;
    
    // Scroll to bottom to show live streaming
    const chatContainer = document.getElementById('chat-messages');
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // Add a small delay to make streaming more visible
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 10);
}

// Finalize streaming message
function finalizeStreamingMessage(messageElement) {
    messageElement.classList.remove('streaming');
    
    // Content should already be formatted from streaming updates
    const textDiv = messageElement.querySelector('.message-text');
    
    // Process any embedded chart containers
    processEmbeddedCharts(messageElement);
}

// Process embedded chart containers
function processEmbeddedCharts(messageElement) {
    // Charts are now embedded as HTML images from the agentic visualizer
    // Just ensure they display properly and scroll to bottom
    const images = messageElement.querySelectorAll('img');
    images.forEach(img => {
        // Ensure images are responsive and properly styled
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
        img.style.display = 'block';
    });
    
    // Scroll to bottom after processing
    const chatContainer = document.getElementById('chat-messages');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}



// Remove streaming message
function removeStreamingMessage(messageElement) {
    if (messageElement && messageElement.parentNode) {
        messageElement.parentNode.removeChild(messageElement);
    }
}

function updateStreamingMessage(messageElement, content) {
    if (messageElement) {
        // Simple markdown-like formatting for common elements
        let formattedContent = content
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^- (.*$)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
            .replace(/\n/g, '<br>');
        
        messageElement.innerHTML = formattedContent;
        processEmbeddedCharts(messageElement);
        finalizeStreamingMessage(messageElement);
    }
}

// Clear conversation
function clearConversation() {
    // Clear chat messages
    const chatContainer = document.getElementById('chat-messages');
    chatContainer.innerHTML = '';
    
    // Reset chat history
    chatHistory = [];
    
    // Call backend to reset agent memory
    fetch('/api/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).catch(error => {
        console.error('Error resetting agent:', error);
    });
}

// Add typing indicator
function addTypingIndicator() {
    const chatContainer = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    const typingId = 'typing-' + Date.now();
    
    typingDiv.id = typingId;
    typingDiv.className = 'chat-message agent';
    typingDiv.innerHTML = `
        <div class="message-content">
            <i class="fas fa-circle-notch fa-spin me-2"></i>
            Thinking...
        </div>
    `;
    
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return typingId;
}

// Remove typing indicator
function removeTypingIndicator(typingId) {
    const typingElement = document.getElementById(typingId);
    if (typingElement) {
        typingElement.remove();
    }
}

// Ask a predefined question
function askQuestion(question) {
    const input = document.getElementById('user-input');
    input.value = question;
    sendMessage();
}

// Update agent statistics
async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (response.ok && data.training_stats) {
            const stats = data.training_stats;
            document.getElementById('interactions').textContent = stats.interactions || 0;
            document.getElementById('confidence').textContent = Math.round((stats.last_confidence || 0) * 100) + '%';
            document.getElementById('memory').textContent = data.memory_size || 0;
        }
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Perform advanced research lookup
async function performResearch(researchType) {
    const input = document.getElementById('user-input');
    const query = input.value.trim();
    
    if (!query) {
        alert('Please enter a search query first.');
        return;
    }
    
    if (isProcessing) return;
    
    isProcessing = true;
    input.disabled = true;
    
    // Research type labels
    const typeLabels = {
        'regulatory': 'FDA Regulatory Updates',
        'clinical_trials': 'Clinical Trials Search',
        'publications': 'Research Publications',
        'statistics': 'Current Statistics',
        'news': 'Industry News',
        'comprehensive': 'Comprehensive Search'
    };
    
    // Add user message to chat
    const userMessage = `🔍 ${typeLabels[researchType]}: ${query}`;
    addMessage(userMessage, 'user');
    
    // Clear input
    input.value = '';
    
    // Create a placeholder for the streaming response
    const responseElement = addStreamingMessage();
    
    try {
        const response = await fetch('/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                type: researchType
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Research request failed');
        }
        
        const data = await response.json();
        
        // Format and display research results
        let formattedResults = `## ${typeLabels[researchType]} Results\n\n`;
        
        if (data.results) {
            // Handle different result structures
            if (data.results.results && Array.isArray(data.results.results)) {
                // Comprehensive search results
                data.results.results.forEach((result, index) => {
                    formattedResults += `### Source ${index + 1}: ${result.source}\n`;
                    formattedResults += `**URL:** ${result.url}\n\n`;
                    if (result.relevant_info) {
                        formattedResults += `${result.relevant_info}\n\n`;
                    }
                    formattedResults += `---\n\n`;
                });
            } else {
                // Other research types
                Object.keys(data.results).forEach(key => {
                    if (key !== 'search_timestamp' && key !== 'query' && key !== 'type') {
                        formattedResults += `### ${key.replace('_', ' ').toUpperCase()}\n`;
                        const items = data.results[key];
                        if (Array.isArray(items)) {
                            items.forEach((item, index) => {
                                formattedResults += `**${index + 1}.** `;
                                if (item.source) formattedResults += `[${item.source}](${item.source})\n`;
                                if (item.relevant_info || item.updates || item.trial_info || item.publication_info || item.statistics || item.news_info) {
                                    const info = item.relevant_info || item.updates || item.trial_info || item.publication_info || item.statistics || item.news_info;
                                    formattedResults += `${info}\n\n`;
                                }
                            });
                        }
                        formattedResults += `---\n\n`;
                    }
                });
            }
        }
        
        formattedResults += `*Research completed at: ${new Date().toLocaleString()}*`;
        
        // Display the formatted results
        updateStreamingMessage(responseElement, formattedResults);
        
    } catch (error) {
        console.error('Research error:', error);
        updateStreamingMessage(responseElement, `❌ **Research Error**: ${error.message}\n\nPlease try again or use a different research method.`);
    } finally {
        isProcessing = false;
        input.disabled = false;
        input.focus();
    }
}

// Perform EHR analysis
async function performEHRAnalysis(analysisType) {
    const input = document.getElementById('user-input');
    const query = input.value.trim();
    
    if (isProcessing) return;
    
    isProcessing = true;
    input.disabled = true;
    
    // Analysis type labels
    const typeLabels = {
        'demographic': 'Demographic Analysis',
        'clinical': 'Clinical Analysis',
        'survival': 'Survival Analysis',
        'predictive': 'Predictive Modeling',
        'network': 'Network Analysis',
        'comprehensive': 'Comprehensive EHR Analysis'
    };
    
    // Data source selection (can be expanded to allow user choice)
    const dataSource = 'synthea'; // Default to Synthea synthetic data
    
    // Add user message to chat
    const userMessage = `🏥 ${typeLabels[analysisType]} using ${dataSource} data`;
    addMessage(userMessage, 'user');
    
    // Clear input
    input.value = '';
    
    // Create a placeholder for the streaming response
    const responseElement = addStreamingMessage();
    
    try {
        const response = await fetch('/ehr/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source: dataSource,
                type: analysisType
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'EHR analysis request failed');
        }
        
        const data = await response.json();
        
        // Format and display EHR analysis results
        let formattedResults = `## ${typeLabels[analysisType]} Results\n\n`;
        formattedResults += `**Data Source:** ${data.data_source}\n`;
        formattedResults += `**Analysis Type:** ${data.analysis_type}\n`;
        formattedResults += `**Processing Time:** ${data.processing_time}\n`;
        formattedResults += `**Patient Count:** ${data.results.patient_count}\n\n`;
        
        // Format results based on analysis type
        if (data.results.demographics) {
            formattedResults += `### Demographics\n`;
            const demo = data.results.demographics;
            formattedResults += `- **Total Patients:** ${demo.total_patients}\n`;
            formattedResults += `- **Mean Age:** ${demo.age_distribution.mean_age} years\n`;
            formattedResults += `- **Gender:** ${demo.gender_distribution.male} male, ${demo.gender_distribution.female} female\n\n`;
            
            formattedResults += `**Age Distribution:**\n`;
            Object.entries(demo.age_distribution.age_ranges).forEach(([range, count]) => {
                formattedResults += `- ${range}: ${count} patients\n`;
            });
            formattedResults += '\n';
        }
        
        if (data.results.clinical_outcomes) {
            formattedResults += `### Clinical Outcomes\n`;
            const clinical = data.results.clinical_outcomes;
            formattedResults += `- **Average Length of Stay:** ${clinical.average_length_of_stay} days\n`;
            formattedResults += `- **Readmission Rate:** ${clinical.readmission_rate}%\n`;
            formattedResults += `- **Mortality Rate:** ${clinical.mortality_rate}%\n\n`;
            
            formattedResults += `**Top Conditions:**\n`;
            clinical.top_conditions.forEach(condition => {
                formattedResults += `- ${condition.condition}: ${condition.prevalence}%\n`;
            });
            formattedResults += '\n';
        }
        
        if (data.results.survival_analysis) {
            formattedResults += `### Survival Analysis\n`;
            const survival = data.results.survival_analysis;
            formattedResults += `- **Median Survival Time:** ${survival.median_survival_time} years\n\n`;
            
            formattedResults += `**Survival Rates:**\n`;
            Object.entries(survival.survival_rates).forEach(([period, rate]) => {
                formattedResults += `- ${period.replace('_', ' ')}: ${(rate * 100).toFixed(1)}%\n`;
            });
            formattedResults += '\n';
            
            if (survival.risk_factors) {
                formattedResults += `**Risk Factors:**\n`;
                survival.risk_factors.forEach(factor => {
                    formattedResults += `- ${factor.factor}: HR ${factor.hazard_ratio}\n`;
                });
                formattedResults += '\n';
            }
        }
        
        if (data.results.predictive_modeling) {
            formattedResults += `### Predictive Modeling\n`;
            const pred = data.results.predictive_modeling;
            formattedResults += `- **Model Accuracy:** ${(pred.model_performance.accuracy * 100).toFixed(1)}%\n`;
            formattedResults += `- **AUC-ROC:** ${pred.model_performance.auc_roc}\n\n`;
            
            formattedResults += `**Risk Categories:**\n`;
            Object.entries(pred.predictions).forEach(([category, count]) => {
                formattedResults += `- ${category.replace('_', ' ')}: ${count} patients\n`;
            });
            formattedResults += '\n';
        }
        
        if (data.results.network_analysis) {
            formattedResults += `### Network Analysis\n`;
            const network = data.results.network_analysis;
            formattedResults += `- **Network Density:** ${network.patient_condition_network.density}\n`;
            formattedResults += `- **Average Clustering:** ${network.patient_condition_network.average_clustering}\n\n`;
        }
        
        if (data.results.comprehensive_analysis) {
            formattedResults += `### Comprehensive Analysis\n`;
            const comp = data.results.comprehensive_analysis;
            formattedResults += `- **Total Patients:** ${comp.patient_demographics.total_patients}\n`;
            formattedResults += `- **Age Range:** ${comp.patient_demographics.age_range}\n`;
            formattedResults += `- **Readmission Rate:** ${comp.outcome_metrics.readmission_rate}%\n`;
            formattedResults += `- **Patient Satisfaction:** ${comp.quality_indicators.patient_satisfaction}/10\n\n`;
        }
        
        // Add key insights if available
        if (data.results.key_insights) {
            formattedResults += `### Key Insights\n`;
            data.results.key_insights.forEach(insight => {
                formattedResults += `- ${insight}\n`;
            });
        }
        
        formattedResults += `*Analysis completed at: ${new Date().toLocaleString()}*`;
        
        // Display the formatted results
        updateStreamingMessage(responseElement, formattedResults);
        
    } catch (error) {
        console.error('EHR analysis error:', error);
        let errorMessage = `❌ **EHR Analysis Error**: ${error.message}\n\n`;
        
        if (error.message.includes('requires full access')) {
            errorMessage += `**Upgrade Required**: EHR analysis capabilities require full access to the system.\n\n`;
            errorMessage += `**Available EHR Analysis Types:**\n`;
            errorMessage += `- 📊 Demographic Analysis - Patient demographics and distributions\n`;
            errorMessage += `- 🏥 Clinical Analysis - Conditions, treatments, and outcomes\n`;
            errorMessage += `- 💓 Survival Analysis - Time-to-event analysis with Kaplan-Meier curves\n`;
            errorMessage += `- 🤖 Predictive Modeling - Machine learning for clinical prediction\n`;
            errorMessage += `- 🔗 Network Analysis - Patient-condition relationship networks\n`;
            errorMessage += `- 📈 Comprehensive Analysis - Complete EHR analysis pipeline\n\n`;
            errorMessage += `**Data Sources Available:**\n`;
            errorMessage += `- Synthea synthetic patient data (~1000 patients)\n`;
            errorMessage += `- MIMIC-style critical care data (~500 patients)\n`;
            errorMessage += `- Custom clinical research dataset (~750 records)\n\n`;
            errorMessage += `Please upgrade to access these powerful EHR analysis capabilities.`;
        } else {
            errorMessage += `Please try again or contact support if the issue persists.`;
        }
        
        updateStreamingMessage(responseElement, errorMessage);
    } finally {
        isProcessing = false;
        input.disabled = false;
        input.focus();
    }
}

// Scrape website for new content
async function scrapeWebsite() {
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    document.getElementById('loading-text').textContent = 'Scraping Crapharma website...';
    loadingModal.show();
    
    try {
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addMessage(`✅ Successfully updated knowledge base with ${data.content_length} characters from ${data.url}`, 'agent');
        } else {
            addMessage(`❌ Failed to update knowledge: ${data.error}`, 'agent');
        }
        
    } catch (error) {
        console.error('Scraping error:', error);
        addMessage('❌ Failed to scrape website. Please try again later.', 'agent');
    } finally {
        loadingModal.hide();
    }
}

// Reset agent
async function resetAgent() {
    if (!confirm('Are you sure you want to reset the agent? This will clear all training progress.')) {
        return;
    }
    
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    document.getElementById('loading-text').textContent = 'Resetting agent...';
    loadingModal.show();
    
    try {
        const response = await fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addMessage('🔄 Agent has been reset successfully. All training progress cleared.', 'agent');
            chatHistory = [];
            updateStats();
        } else {
            addMessage(`❌ Failed to reset agent: ${data.error}`, 'agent');
        }
        
    } catch (error) {
        console.error('Reset error:', error);
        addMessage('❌ Failed to reset agent. Please try again later.', 'agent');
    } finally {
        loadingModal.hide();
    }
}

// Utility function to format confidence as percentage
function formatConfidence(confidence) {
    return Math.round((confidence || 0) * 100) + '%';
}

// Utility function to format timestamp
function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
}

// Clear conversation function
function clearConversation() {
    if (confirm('Are you sure you want to clear the conversation?')) {
        const chatContainer = document.getElementById('chat-messages');
        chatContainer.innerHTML = '';
        chatHistory = [];
        console.log('Conversation cleared');
    }
}

// Handle window resize for responsive chat
window.addEventListener('resize', function() {
    const chatContainer = document.getElementById('chat-messages');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});

// MRI Analysis Functions
async function performMRIAnalysis(analysisType) {
    const input = document.getElementById('user-input');
    
    if (isProcessing) return;
    
    isProcessing = true;
    input.disabled = true;
    
    // Analysis type labels
    const typeLabels = {
        'analyze_dataset': 'Complete Dataset Analysis (18 scans)',
        'classify_single': 'Single Scan Classification', 
        'generate_synthetic': 'Synthetic Data Generation'
    };
    
    // Add user message to chat
    const userMessage = `🧠 MRI Analysis: ${typeLabels[analysisType]}`;
    addMessage(userMessage, 'user');
    
    // Clear input
    input.value = '';
    
    // Create a placeholder for the streaming response
    const responseElement = addStreamingMessage();
    
    try {
        let requestBody = { action: analysisType };
        
        // Handle single scan classification
        if (analysisType === 'classify_single') {
            const files = await getMRIFiles();
            if (files.length === 0) {
                throw new Error('No MRI files found for classification');
            }
            // Use the first file as example
            requestBody.filename = files[0].filename;
        }
        
        // Handle synthetic generation
        if (analysisType === 'generate_synthetic') {
            requestBody.n_samples = 5; // Generate 5 synthetic samples
        }
        
        const response = await fetch('/api/mri-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'MRI analysis request failed');
        }
        
        const data = await response.json();
        
        // Format and display MRI analysis results
        let formattedResults = `## ${typeLabels[analysisType]} Results\n\n`;
        
        if (analysisType === 'analyze_dataset') {
            formattedResults += `**Dataset Analysis Complete**\n`;
            formattedResults += `- Files analyzed: ${data.results.files_analyzed}\n`;
            formattedResults += `- Features extracted: ${data.results.features_extracted}\n`;
            formattedResults += `- Anomaly detection: ${data.results.anomaly_detection}\n`;
            formattedResults += `- Clustering: ${data.results.clustering}\n`;
            formattedResults += `- Models trained: ${data.results.models_trained.join(', ')}\n\n`;
            
            if (data.results.report) {
                formattedResults += `### Analysis Report\n`;
                formattedResults += data.results.report;
            }
        } else if (analysisType === 'classify_single') {
            formattedResults += `**Single Scan Classification**\n`;
            formattedResults += `- File: ${data.filename}\n`;
            formattedResults += `- Classification: ${data.classification.classification}\n`;
            formattedResults += `- Confidence: ${(data.classification.confidence * 100).toFixed(1)}%\n`;
            formattedResults += `- Anomaly Score: ${data.classification.anomaly_score.toFixed(3)}\n`;
            formattedResults += `- Control Group: ${data.classification.is_control ? 'Yes' : 'No'}\n`;
            
            if (data.classification.cluster_label !== null) {
                formattedResults += `- Cluster: ${data.classification.cluster_label}\n`;
            }
        } else if (analysisType === 'generate_synthetic') {
            formattedResults += `**Synthetic Data Generation**\n`;
            formattedResults += `- Generated samples: ${data.data_shape[0]}\n`;
            formattedResults += `- Features per sample: ${data.data_shape[1]}\n`;
            formattedResults += `- Method: ${data.method}\n`;
            formattedResults += `- Based on: ${data.original_samples} original scans\n`;
            formattedResults += `\n**Note**: Synthetic data represents feature variations of the control group for analysis purposes.\n`;
        }
        
        formattedResults += `\n---\n\n`;
        formattedResults += `**Technical Details:**\n`;
        formattedResults += `- Analysis uses traditional machine learning (scikit-learn)\n`;
        formattedResults += `- Features include statistical moments, texture, and regional analysis\n`;
        formattedResults += `- Anomaly detection via Isolation Forest\n`;
        formattedResults += `- Clustering via K-means with PCA dimensionality reduction\n\n`;
        
        formattedResults += `*Analysis completed at: ${new Date().toLocaleString()}*`;
        
        // Display the formatted results
        updateStreamingMessage(responseElement, formattedResults);
        
    } catch (error) {
        console.error('MRI analysis error:', error);
        let errorMessage = `❌ **MRI Analysis Error**: ${error.message}\n\n`;
        
        if (error.message.includes('not available')) {
            errorMessage += `**System Requirements**: MRI analysis requires neuroimaging libraries.\n\n`;
            errorMessage += `**Available MRI Analysis Features:**\n`;
            errorMessage += `- 🧠 Complete Dataset Analysis - Process all 18 control scans\n`;
            errorMessage += `- 🔍 Single Scan Classification - Classify individual scans\n`;
            errorMessage += `- ✨ Synthetic Data Generation - Create variations for analysis\n`;
            errorMessage += `- 📊 Feature Extraction - 77 neuroimaging features per scan\n`;
            errorMessage += `- 🎯 Anomaly Detection - Identify unusual patterns\n`;
            errorMessage += `- 🧮 Clustering Analysis - Group similar scans\n\n`;
            errorMessage += `**Control Group Data**: 18 healthy T1-weighted anatomical MRI scans available for analysis.`;
        } else {
            errorMessage += `Please try again or contact support if the issue persists.`;
        }
        
        updateStreamingMessage(responseElement, errorMessage);
    } finally {
        isProcessing = false;
        input.disabled = false;
        input.focus();
    }
}

// Show MRI Files
async function showMRIFiles() {
    const input = document.getElementById('user-input');
    
    if (isProcessing) return;
    
    isProcessing = true;
    input.disabled = true;
    
    // Add user message to chat
    const userMessage = `📁 View MRI Files`;
    addMessage(userMessage, 'user');
    
    // Create a placeholder for the streaming response
    const responseElement = addStreamingMessage();
    
    try {
        const files = await getMRIFiles();
        
        let formattedResults = `## MRI Dataset Files\n\n`;
        formattedResults += `**Total Files**: ${files.length}\n`;
        formattedResults += `**File Format**: NIfTI (.nii.gz) and JSON metadata\n`;
        formattedResults += `**Data Type**: T1-weighted anatomical MRI scans\n`;
        formattedResults += `**Population**: Healthy control group\n\n`;
        
        formattedResults += `### File Details\n`;
        
        let totalSize = 0;
        let niftiCount = 0;
        let jsonCount = 0;
        
        files.forEach((file, index) => {
            const subjectId = file.filename.match(/sub-(\d+)/)?.[1] || 'unknown';
            const fileType = file.type === 'json' ? 'JSON metadata' : 'NIfTI scan';
            
            if (file.type === 'json') {
                jsonCount++;
            } else {
                niftiCount++;
            }
            
            formattedResults += `${index + 1}. **Subject ${subjectId}** (${fileType})\n`;
            formattedResults += `   - File: ${file.filename}\n`;
            formattedResults += `   - Size: ${file.size_mb} MB\n`;
            totalSize += file.size_mb;
        });
        
        formattedResults += `\n**File Summary:**\n`;
        formattedResults += `- NIfTI scans: ${niftiCount}\n`;
        formattedResults += `- JSON metadata: ${jsonCount}\n`;
        formattedResults += `**Total Dataset Size**: ${totalSize.toFixed(2)} MB\n\n`;
        
        formattedResults += `### Analysis Capabilities\n`;
        formattedResults += `- Extract 77 neuroimaging features per scan\n`;
        formattedResults += `- Perform anomaly detection (control vs non-control)\n`;
        formattedResults += `- Cluster similar brain patterns\n`;
        formattedResults += `- Generate synthetic variations for analysis\n`;
        formattedResults += `- Classify individual scans\n\n`;
        
        formattedResults += `*File listing generated at: ${new Date().toLocaleString()}*`;
        
        // Display the formatted results
        updateStreamingMessage(responseElement, formattedResults);
        
    } catch (error) {
        console.error('MRI files error:', error);
        updateStreamingMessage(responseElement, `❌ **Error**: ${error.message}\n\nCould not retrieve MRI file list.`);
    } finally {
        isProcessing = false;
        input.disabled = false;
        input.focus();
    }
}

// Helper function to get MRI files
async function getMRIFiles() {
    const response = await fetch('/api/mri-files');
    if (!response.ok) {
        throw new Error('Failed to fetch MRI files');
    }
    const data = await response.json();
    return data.files || [];
}

// Analyze MRI files function
async function analyzeMRIFiles(files) {
    const input = document.getElementById('user-input');
    
    if (isProcessing) return;
    
    isProcessing = true;
    input.disabled = true;
    
    // Add user message to chat
    let fileList = Array.from(files).map(f => f.name).join(', ');
    const userMessage = `🧠 Analyzing MRI files: ${fileList}`;
    addMessage(userMessage, 'user');
    
    // Create a placeholder for the streaming response
    const responseElement = addStreamingMessage();
    
    try {
        const formData = new FormData();
        
        // Add all files to form data
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }
        
        const response = await fetch('/api/upload-mri', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'MRI analysis failed');
        }
        
        const data = await response.json();
        
        // Format analysis results
        let formattedResults = `## MRI Analysis Results\n\n`;
        formattedResults += `**Files Analyzed**: ${data.uploaded_files.length}\n`;
        formattedResults += `**Total Size**: ${(data.total_size / (1024 * 1024)).toFixed(2)} MB\n\n`;
        
        formattedResults += `### File Analysis:\n`;
        data.uploaded_files.forEach((file, index) => {
            const fileType = file.name.endsWith('.json') ? 'JSON metadata' : 'MRI scan';
            formattedResults += `${index + 1}. **${file.name}** (${file.size_mb} MB) - ${fileType}\n`;
        });
        
        if (data.processing_results) {
            formattedResults += `\n### Processing Results:\n`;
            data.processing_results.forEach(result => {
                if (result.type === 'nifti') {
                    formattedResults += `- **${result.filename}**: ${result.features_extracted} neuroimaging features extracted\n`;
                    formattedResults += `  - Image dimensions: ${result.dimensions}\n`;
                    formattedResults += `  - Voxel size: ${result.voxel_size}\n`;
                } else if (result.type === 'json') {
                    formattedResults += `- **${result.filename}**: Metadata parsed - ${result.metadata_fields} fields\n`;
                }
            });
        }
        
        formattedResults += `\n---\n\n`;
        formattedResults += `**Analysis Capabilities:**\n`;
        formattedResults += `- Statistical feature extraction (mean, std, skewness, kurtosis)\n`;
        formattedResults += `- Texture analysis using Gray Level Co-occurrence Matrix\n`;
        formattedResults += `- Regional brain analysis and segmentation\n`;
        formattedResults += `- Anomaly detection using Isolation Forest\n`;
        formattedResults += `- Clustering analysis with K-means\n`;
        formattedResults += `- Classification: Control vs Non-control\n\n`;
        
        formattedResults += `**Next Steps:**\n`;
        formattedResults += `- Files are now ready for detailed analysis\n`;
        formattedResults += `- Ask me specific questions about the MRI data\n`;
        formattedResults += `- Request classification of individual scans\n`;
        formattedResults += `- Generate synthetic variations for research\n\n`;
        
        formattedResults += `*Analysis completed at: ${new Date().toLocaleString()}*`;
        
        // Clear the file input
        document.getElementById('mriFileInput').value = '';
        
        // Display the formatted results
        updateStreamingMessage(responseElement, formattedResults);
        
    } catch (error) {
        console.error('MRI analysis error:', error);
        let errorMessage = `❌ **MRI Analysis Error**: ${error.message}\n\n`;
        
        if (error.message.includes('file size')) {
            errorMessage += `**File Size Limit**: Please ensure files are under the maximum allowed size.\n`;
        } else if (error.message.includes('format')) {
            errorMessage += `**Supported Formats**: .nii, .nii.gz, .json\n`;
        } else {
            errorMessage += `**Supported File Types:**\n`;
            errorMessage += `- .nii.gz - Compressed NIfTI MRI scans\n`;
            errorMessage += `- .nii - Uncompressed NIfTI MRI scans\n`;
            errorMessage += `- .json - MRI acquisition metadata\n\n`;
            errorMessage += `Please ensure files are in the correct format and try again.`;
        }
        
        updateStreamingMessage(responseElement, errorMessage);
    } finally {
        isProcessing = false;
        input.disabled = false;
        input.focus();
    }
}

// Upload MRI files function
async function uploadMRIFiles(files) {
    const input = document.getElementById('user-input');
    
    if (isProcessing) return;
    
    isProcessing = true;
    input.disabled = true;
    
    // Add user message to chat
    let fileList = Array.from(files).map(f => f.name).join(', ');
    const userMessage = `🧠 Uploading MRI files: ${fileList}`;
    addMessage(userMessage, 'user');
    
    // Create a placeholder for the streaming response
    const responseElement = addStreamingMessage();
    
    try {
        const formData = new FormData();
        
        // Add all files to form data
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }
        
        const response = await fetch('/api/upload-mri', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'MRI upload failed');
        }
        
        const data = await response.json();
        
        // Format upload results
        let formattedResults = `## MRI Files Upload Complete\n\n`;
        formattedResults += `**Files Uploaded**: ${data.uploaded_files.length}\n`;
        formattedResults += `**Total Size**: ${(data.total_size / (1024 * 1024)).toFixed(2)} MB\n\n`;
        
        formattedResults += `### Uploaded Files:\n`;
        data.uploaded_files.forEach((file, index) => {
            const fileType = file.name.endsWith('.json') ? 'JSON metadata' : 'NIfTI scan';
            formattedResults += `${index + 1}. **${file.name}** (${file.size_mb} MB) - ${fileType}\n`;
        });
        
        if (data.processing_results) {
            formattedResults += `\n### Processing Results:\n`;
            data.processing_results.forEach(result => {
                if (result.type === 'nifti') {
                    formattedResults += `- **${result.filename}**: ${result.features_extracted} features extracted\n`;
                } else if (result.type === 'json') {
                    formattedResults += `- **${result.filename}**: Metadata parsed - ${result.metadata_fields} fields\n`;
                }
            });
        }
        
        formattedResults += `\n---\n\n`;
        formattedResults += `**Next Steps:**\n`;
        formattedResults += `- Use "Analyze Dataset" to process all uploaded scans\n`;
        formattedResults += `- Use "Classify Single Scan" to analyze individual files\n`;
        formattedResults += `- Use "Generate Synthetic" to create variations\n`;
        formattedResults += `- JSON metadata will be used to enhance analysis accuracy\n\n`;
        
        formattedResults += `*Upload completed at: ${new Date().toLocaleString()}*`;
        
        // Clear the file input
        document.getElementById('mriFileInput').value = '';
        
        // Display the formatted results
        updateStreamingMessage(responseElement, formattedResults);
        
    } catch (error) {
        console.error('MRI upload error:', error);
        let errorMessage = `❌ **MRI Upload Error**: ${error.message}\n\n`;
        
        if (error.message.includes('file size')) {
            errorMessage += `**File Size Limit**: Please ensure files are under the maximum allowed size.\n`;
        } else if (error.message.includes('format')) {
            errorMessage += `**Supported Formats**: .nii, .nii.gz, .json\n`;
        } else {
            errorMessage += `**Supported File Types:**\n`;
            errorMessage += `- .nii.gz - Compressed NIfTI MRI scans\n`;
            errorMessage += `- .nii - Uncompressed NIfTI MRI scans\n`;
            errorMessage += `- .json - MRI acquisition metadata\n\n`;
            errorMessage += `Please ensure files are in the correct format and try again.`;
        }
        
        updateStreamingMessage(responseElement, errorMessage);
    } finally {
        isProcessing = false;
        input.disabled = false;
        input.focus();
    }
}


// Pinned Files Functions

// Flexible MRI Analysis Functions
function showFlexibleMRIModal() {
    const modal = new bootstrap.Modal(document.getElementById("flexibleMRIModal"));
    modal.show();
    
    // Initialize sliders
    const contrastSlider = document.getElementById("contrastSlider");
    const brightnessSlider = document.getElementById("brightnessSlider");
    const coordinateSelect = document.getElementById("coordinateSystemSelect");
    
    if (contrastSlider) {
        contrastSlider.addEventListener("input", function() {
            document.getElementById("contrastValue").textContent = this.value;
        });
    }
    
    if (brightnessSlider) {
        brightnessSlider.addEventListener("input", function() {
            document.getElementById("brightnessValue").textContent = this.value;
        });
    }
    
    if (coordinateSelect) {
        coordinateSelect.addEventListener("change", function() {
            const customPanel = document.getElementById("customCoordinatesPanel");
            if (this.value === "custom") {
                customPanel.style.display = "block";
            } else {
                customPanel.style.display = "none";
            }
        });
    }
}

function showCoordinateSystemsModal() {
    const modal = new bootstrap.Modal(document.getElementById("coordinateSystemsModal"));
    modal.show();
    
    // Load coordinate systems info
    loadCoordinateSystemsInfo();
}

async function loadCoordinateSystemsInfo() {
    try {
        const response = await fetch("/api/coordinate-systems");
        const data = await response.json();
        
        const infoDiv = document.getElementById("coordinateSystemsInfo");
        
        if (data.success) {
            let html = "<div class=\"row g-3\">";
            
            for (const [key, system] of Object.entries(data.coordinate_systems)) {
                html += `
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h6 class="card-title">${system.name}</h6>
                                <p class="card-text">${system.description}</p>
                                <p class="text-muted"><small><strong>Use case:</strong> ${system.use_case}</small></p>
                                <div class="mt-2">
                                    <small class="text-muted">
                                        <strong>Coordinates:</strong><br>
                                        X: ${system.coordinates.x[0]} - ${system.coordinates.x[1] || "Max"}<br>
                                        Y: ${system.coordinates.y[0]} - ${system.coordinates.y[1] || "Max"}<br>
                                        Z: ${system.coordinates.z[0]} - ${system.coordinates.z[1] || "Max"}
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            html += "</div>";
            infoDiv.innerHTML = html;
        } else {
            infoDiv.innerHTML = "<div class=\"alert alert-danger\">Failed to load coordinate systems information</div>";
        }
    } catch (error) {
        console.error("Error loading coordinate systems:", error);
        document.getElementById("coordinateSystemsInfo").innerHTML = 
            "<div class=\"alert alert-danger\">Error loading coordinate systems information</div>";
    }
}

async function runFlexibleMRIAnalysis() {
    const resultsDiv = document.getElementById("mriAnalysisResults");
    const coordinateSystem = document.getElementById("coordinateSystemSelect").value;
    
    // Show loading state
    resultsDiv.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Running flexible MRI analysis...</p>
        </div>
    `;
    
    try {
        // Prepare request data
        const requestData = {
            coordinate_system: coordinateSystem,
            visualization_params: {
                contrast_adjustment: parseFloat(document.getElementById("contrastSlider").value),
                brightness_adjustment: parseFloat(document.getElementById("brightnessSlider").value),
                color_map: document.getElementById("colorMapSelect").value
            }
        };
        
        // Add custom coordinates if selected
        if (coordinateSystem === "custom") {
            requestData.custom_coords = {
                x: [parseInt(document.getElementById("xMin").value), parseInt(document.getElementById("xMax").value)],
                y: [parseInt(document.getElementById("yMin").value), parseInt(document.getElementById("yMax").value)],
                z: [parseInt(document.getElementById("zMin").value), parseInt(document.getElementById("zMax").value)]
            };
        }
        
        const response = await fetch("/api/flexible-mri-analysis", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display results
            let html = "<div class=\"analysis-results\">";
            
            // Show visualization if available
            if (data.visualization) {
                html += `
                    <div class="mb-3">
                        <h6>Visualization:</h6>
                        <img src="data:image/png;base64,${data.visualization}" class="img-fluid" alt="MRI Visualization">
                    </div>
                `;
            }
            
            // Show analysis summary
            if (data.analysis_summary) {
                const summary = data.analysis_summary;
                html += `
                    <div class="mb-3">
                        <h6>Analysis Summary:</h6>
                        <div class="row g-2">
                            <div class="col-12">
                                <small class="text-muted">
                                    <strong>Coordinate System:</strong> ${summary.coordinate_system}<br>
                                    <strong>Scans Processed:</strong> ${summary.total_scans}<br>
                                    <strong>Average Shape:</strong> ${summary.average_shape.join(" × ")}<br>
                                    <strong>Data Reduction:</strong> ${(summary.data_reduction_info.reduction_ratio * 100).toFixed(1)}%
                                </small>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            // Show coverage analysis if available
            if (data.coverage_analysis) {
                const coverage = data.coverage_analysis;
                html += `
                    <div class="mb-3">
                        <h6>Coverage Analysis:</h6>
                        <div class="progress mb-2">
                            <div class="progress-bar" role="progressbar" style="width: ${coverage.average_coverage * 100}%">
                                ${(coverage.average_coverage * 100).toFixed(1)}% Coverage
                            </div>
                        </div>
                        <small class="text-muted">${coverage.recommendation}</small>
                    </div>
                `;
            }
            
            html += "</div>";
            resultsDiv.innerHTML = html;
            
        } else {
            resultsDiv.innerHTML = `
                <div class="alert alert-danger">
                    <h6>Analysis Failed</h6>
                    <p>${data.error || "Unknown error occurred"}</p>
                </div>
            `;
        }
        
    } catch (error) {
        console.error("Error running flexible MRI analysis:", error);
        resultsDiv.innerHTML = `
            <div class="alert alert-danger">
                <h6>Error</h6>
                <p>Failed to run flexible MRI analysis: ${error.message}</p>
            </div>
        `;
    }
}

// Medical Co-pilot PDF Upload Functions
function uploadPDFToMedicalCopilot() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf';
    input.onchange = function(event) {
        const file = event.target.files[0];
        if (file) {
            processMedicalPDF(file);
        }
    };
    input.click();
}

async function processMedicalPDF(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload-medical-pdf', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display extracted text in appropriate modal
            const activeModal = document.querySelector('.modal.show');
            if (activeModal) {
                const textarea = activeModal.querySelector('textarea');
                if (textarea) {
                    textarea.value = data.extracted_text;
                }
            }
            
            // Show success message
            showNotification(`PDF "${file.name}" processed successfully. Text extracted and ready for analysis.`, 'success');
        } else {
            showNotification(`Failed to process PDF: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error processing PDF:', error);
        showNotification(`Error processing PDF: ${error.message}`, 'error');
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Tab switching functionality
function switchTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content-panel');
    tabContents.forEach(content => {
        content.style.display = 'none';
    });
    
    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.nav-link');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab content
    const selectedContent = document.getElementById(tabName + '-content');
    if (selectedContent) {
        selectedContent.style.display = 'block';
    }
    
    // Add active class to selected tab
    const selectedTab = document.getElementById(tabName + '-tab');
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
}

// Initialize tabs on page load
document.addEventListener('DOMContentLoaded', function() {
    // Show main tab by default
    switchTab('main');
});

// Medical Co-pilot Modal Functions
function showMedicalQueryModal() {
    const modal = new bootstrap.Modal(document.getElementById("medicalQueryModal"));
    modal.show();
}

function showRecordInterpretationModal() {
    const modal = new bootstrap.Modal(document.getElementById("recordInterpretationModal"));
    modal.show();
}

function showFHIRModal() {
    const modal = new bootstrap.Modal(document.getElementById("fhirModal"));
    modal.show();
}

function showDeidentifyModal() {
    const modal = new bootstrap.Modal(document.getElementById("deidentifyModal"));
    modal.show();
}

function showClinicalSummaryModal() {
    const modal = new bootstrap.Modal(document.getElementById("clinicalSummaryModal"));
    modal.show();
}

function showPriorAuthModal() {
    const modal = new bootstrap.Modal(document.getElementById("priorAuthModal"));
    modal.show();
}

function showPatientExplanationModal() {
    const modal = new bootstrap.Modal(document.getElementById("patientExplanationModal"));
    modal.show();
}

function showTimelineModal() {
    const modal = new bootstrap.Modal(document.getElementById("timelineModal"));
    modal.show();
}

function showRiskScoreModal() {
    const modal = new bootstrap.Modal(document.getElementById("riskScoreModal"));
    modal.show();
}

function showClaimFormatterModal() {
    const modal = new bootstrap.Modal(document.getElementById("claimFormatterModal"));
    modal.show();
}

async function generateSQL() {
    const query = document.getElementById('medicalQuery').value;
    const sqlTextarea = document.getElementById('generatedSQL');
    
    if (!query) {
        alert('Please enter a natural language query');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/text-to-sql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            sqlTextarea.value = data.sql_query;
        } else {
            alert('Error generating SQL: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function executeQuery() {
    const sqlQuery = document.getElementById('generatedSQL').value;
    const resultsDiv = document.getElementById('queryResults');
    
    if (!sqlQuery) {
        alert('Please generate SQL first');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/execute-query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: sqlQuery })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            const table = document.getElementById('resultsTable');
            
            // Clear previous results
            table.innerHTML = '';
            
            if (data.results.length > 0) {
                // Create header
                const headerRow = table.insertRow();
                Object.keys(data.results[0]).forEach(key => {
                    const th = document.createElement('th');
                    th.textContent = key;
                    headerRow.appendChild(th);
                });
                
                // Create data rows
                data.results.forEach(row => {
                    const dataRow = table.insertRow();
                    Object.values(row).forEach(value => {
                        const td = dataRow.insertCell();
                        td.textContent = value;
                    });
                });
            } else {
                table.innerHTML = '<tr><td>No results found</td></tr>';
            }
        } else {
            alert('Error executing query: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function interpretRecord() {
    const recordText = document.getElementById('recordText').value;
    const resultsDiv = document.getElementById('interpretationResults');
    
    if (!recordText) {
        alert('Please enter medical record text');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/interpret-record', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: recordText })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            const contentDiv = document.getElementById('interpretationContent');
            contentDiv.innerHTML = `<pre>${data.interpretation}</pre>`;
        } else {
            alert('Error interpreting record: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function createFHIR() {
    const patientData = document.getElementById('patientData').value;
    const resultsDiv = document.getElementById('fhirResults');
    
    if (!patientData) {
        alert('Please enter patient data');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/create-fhir', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ patient_data: patientData })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            const contentPre = document.getElementById('fhirContent');
            contentPre.textContent = JSON.stringify(data.fhir_resource, null, 2);
        } else {
            alert('Error creating FHIR resource: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function deidentifyText() {
    const medicalText = document.getElementById('medicalText').value;
    const resultsDiv = document.getElementById('deidentifyResults');
    
    if (!medicalText) {
        alert('Please enter medical text');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/deidentify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: medicalText })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            const textarea = document.getElementById('deidentifiedText');
            textarea.value = data.deidentified_text;
        } else {
            alert('Error de-identifying text: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// New EHR Tool Functions
async function generateClinicalSummary() {
    const encounterNotes = document.getElementById('encounterNotes').value;
    const summaryType = document.getElementById('summaryType').value;
    const resultsDiv = document.getElementById('summaryResults');
    
    if (!encounterNotes) {
        alert('Please enter patient encounter notes');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/generate-clinical-summary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                encounter_notes: encounterNotes,
                summary_type: summaryType
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            document.getElementById('summaryContent').innerHTML = `<pre>${data.summary}</pre>`;
        } else {
            alert('Error generating clinical summary: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function generatePriorAuth() {
    const priorAuthNotes = document.getElementById('priorAuthNotes').value;
    const resultsDiv = document.getElementById('priorAuthResults');
    
    if (!priorAuthNotes) {
        alert('Please enter medical documentation');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/generate-prior-auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ medical_notes: priorAuthNotes })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            document.getElementById('priorAuthContent').innerHTML = `<pre>${data.prior_auth_package}</pre>`;
        } else {
            alert('Error generating prior authorization: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function generatePatientExplanation() {
    const medicalRecords = document.getElementById('medicalRecordsExplain').value;
    const resultsDiv = document.getElementById('patientExplanationResults');
    
    if (!medicalRecords) {
        alert('Please enter medical records or diagnosis');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/generate-patient-explanation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ medical_records: medicalRecords })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            document.getElementById('patientExplanationContent').innerHTML = `<pre>${data.patient_explanation}</pre>`;
        } else {
            alert('Error generating patient explanation: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function generateTimeline() {
    const patientHistory = document.getElementById('patientHistoryData').value;
    const resultsDiv = document.getElementById('timelineResults');
    
    if (!patientHistory) {
        alert('Please enter patient history data');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/generate-timeline', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ patient_history: patientHistory })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            document.getElementById('timelineContent').innerHTML = data.timeline_html;
        } else {
            alert('Error generating timeline: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function calculateRiskScore() {
    const riskData = document.getElementById('riskAssessmentData').value;
    const riskType = document.getElementById('riskScoreType').value;
    const resultsDiv = document.getElementById('riskScoreResults');
    
    if (!riskData) {
        alert('Please enter patient clinical data');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/calculate-risk-score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                clinical_data: riskData,
                risk_type: riskType
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            document.getElementById('riskScoreContent').innerHTML = `<pre>${data.risk_assessment}</pre>`;
        } else {
            alert('Error calculating risk score: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function formatClaim() {
    const ehrData = document.getElementById('ehrClaimData').value;
    const claimType = document.getElementById('claimFormType').value;
    const resultsDiv = document.getElementById('claimFormatterResults');
    
    if (!ehrData) {
        alert('Please enter EHR entry data');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/format-claim', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                ehr_data: ehrData,
                claim_type: claimType
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultsDiv.style.display = 'block';
            document.getElementById('claimFormatterContent').innerHTML = `<pre>${data.claim_form}</pre>`;
        } else {
            alert('Error formatting claim: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// MRI Analysis Functions
async function analyzeMRIFiles(files) {
    const formData = new FormData();
    
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }
    
    try {
        const response = await fetch('/api/upload-mri', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display results in chat
            const message = `MRI Analysis Results:\n\n${data.analysis_text}`;
            displayMessage(message, 'assistant');
        } else {
            alert('Error analyzing MRI files: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}
