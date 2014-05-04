#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	listen
Summary:	Listen to file modifications
Name:		ruby-%{pkgname}
Version:	0.4.7
Release:	0.4
License:	MIT
Group:		Development/Languages
Source0:	https://github.com/guard/listen/archive/v%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	4fd1549ecf72c0ec84659fb28bd15833
Patch0:		deps.patch
URL:		https://github.com/guard/listen
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
BuildRequires:	ruby-bundler
BuildRequires:	ruby-rspec
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Listen gem listens to file modifications and notifies you about
the changes. Works everywhere!

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

%if %{with tests}
rspec spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
